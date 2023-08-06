# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Bliss REPL (Read Eval Print Loop)"""

import asyncio
from typing import Optional
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

import re
import os
import sys
import types
import socket
import functools
import gevent
import signal
import logging
import platform
from collections import deque
from datetime import datetime

import ptpython.layout
from prompt_toolkit.patch_stdout import (
    patch_stdout as patch_stdout_context,
    StdoutProxy,
)
from prompt_toolkit import patch_stdout as patch_stdout_module
from prompt_toolkit.output import DummyOutput

# imports needed to have control over _execute of ptpython
from prompt_toolkit.keys import Keys
from prompt_toolkit.utils import is_windows
from prompt_toolkit.filters import has_focus
from prompt_toolkit.enums import DEFAULT_BUFFER

from .. import log_utils
from bliss.shell.cli.prompt import BlissPrompt
from bliss.shell.cli.typing_helper import TypingHelper
from bliss.shell.cli.ptpython_statusbar_patch import NEWstatus_bar, TMUXstatus_bar
from bliss.shell.bliss_banners import print_rainbow_banner
from bliss.shell.cli.protected_dict import ProtectedDict
from bliss.shell.cli.no_thread_repl import NoThreadPythonRepl
from bliss.shell.cli.formatted_traceback import BlissTraceback, pprint_traceback
from bliss.shell import standard

from bliss import set_bliss_shell_mode
from bliss.common.utils import Singleton
from bliss.common.utils import BLUE
from bliss.common import constants
from bliss.common import session as session_mdl
from bliss.common.session import DefaultSession
from bliss import release, current_session
from bliss.config import static
from bliss.config.conductor.client import get_default_connection
from bliss.shell.standard import info
from bliss.common.logtools import userlogger, elogbook
from bliss.common.protocols import ErrorReportInterface, HasInfo

from bliss.physics.units import ur

logger = logging.getLogger(__name__)


class BlissStdoutProxy(StdoutProxy):
    def _write(self, data: str):
        res = super()._write(data)
        if "\r" in data:
            self.flush()
        return res


patch_stdout_module.StdoutProxy = BlissStdoutProxy


session_mdl.set_current_session = functools.partial(
    session_mdl.set_current_session, force=False
)


# =================== ERROR REPORTING ============================


class ErrorReport(ErrorReportInterface):
    """
    Manage the behavior of the error reporting in the shell.

    - ErrorReport.expert_mode = False (default) => prints a user friendly error message without traceback
    - ErrorReport.expert_mode = True            => prints the full error message with traceback

    - ErrorReport.last_error stores the last error traceback

    """

    _orig_sys_excepthook = sys.excepthook
    _orig_gevent_print_exception = gevent.hub.Hub.print_exception

    def __init__(self):
        self._expert_mode = False
        self._history = deque(maxlen=100)

    @property
    def history(self):
        return self._history

    @property
    def expert_mode(self):
        return self._expert_mode

    @expert_mode.setter
    def expert_mode(self, enable):
        self._expert_mode = bool(enable)


def install_excepthook():
    """Patch the system exception hook,
    and the print exception for gevent greenlet
    """
    error_report = ErrorReport()

    exc_logger = logging.getLogger("exceptions")

    def repl_excepthook(exc_type, exc_value, tb, _with_elogbook=True):
        if exc_value is None:
            # filter exceptions from asyncio_gevent(?) with no traceback, no value
            return

        # BlissTraceback captures traceback information without holding any reference on its content
        fmt_tb = BlissTraceback(exc_type, exc_value, tb)

        # store BlissTraceback for later formatting
        error_report.history.append(fmt_tb)

        # publish full error to logger
        exc_logger.error(fmt_tb.format(disable_blacklist=True))

        # Adapt the error message depending on the expert_mode
        if error_report._expert_mode:
            fmt_tb = error_report.history[-1].format(disable_blacklist=True)
            try:
                style = BlissRepl()._current_style
            except Exception:
                # BlissRepl singleton is not instantiated yet
                # falling back to monochrome
                print(fmt_tb)
            else:
                pprint_traceback(fmt_tb, style)
        elif current_session:
            if current_session.is_loading_config:
                print(f"{exc_type.__name__}: {exc_value}", file=sys.stderr)
            else:
                print(
                    f"!!! === {exc_type.__name__}: {exc_value} === !!! ( for more details type cmd 'last_error()' )",
                    file=sys.stderr,
                )

        if _with_elogbook:
            try:
                elogbook.error(f"{exc_type.__name__}: {exc_value}")
            except Exception:
                repl_excepthook(*sys.exc_info(), _with_elogbook=False)

    def print_exception(self, context, exc_type, exc_value, tb):
        if gevent.getcurrent() is self:
            # repl_excepthook tries to yield to the gevent loop
            gevent.spawn(repl_excepthook, exc_type, exc_value, tb)
        else:
            repl_excepthook(exc_type, exc_value, tb)

    sys.excepthook = repl_excepthook
    gevent.hub.Hub.print_exception = types.MethodType(print_exception, gevent.get_hub())
    return error_report


def reset_excepthook():
    sys.excepthook = ErrorReport._orig_sys_excepthook
    gevent.hub.Hub.print_exception = ErrorReport._orig_gevent_print_exception


__all__ = ("BlissRepl", "embed", "cli", "configure_repl")

#############
# patch ptpython signaturetoolbar
import bliss.shell.cli.ptpython_signature_patch  # noqa: F401,E402

# patch ptpython completer, and jedi
import bliss.shell.cli.ptpython_completer_patch  # noqa: F401,E402

#############


class WrappedStdout:
    def __init__(self, output_buffer):
        self._buffer = output_buffer
        self._orig_stdout = sys.stdout

    # context manager
    def __enter__(self, *args, **kwargs):
        self._orig_stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, *args, **kwargs):
        sys.stdout = self._orig_stdout

    # delegated members
    @property
    def encoding(self):
        return self._orig_stdout.encoding

    @property
    def errors(self):
        return self._orig_stdout.errors

    def fileno(self) -> int:
        # This is important for code that expects sys.stdout.fileno() to work.
        return self._orig_stdout.fileno()

    def isatty(self) -> bool:
        return self._orig_stdout.isatty()

    def flush(self):
        self._orig_stdout.flush()

    # extended members
    def write(self, data):
        # wait for stdout to be ready to receive output
        if True:  # if gevent.select.select([],[self.fileno()], []):
            self._buffer.append(data)
            self._orig_stdout.write(data)


class PromptToolkitOutputWrapper(DummyOutput):
    """This class is used to keep track of the output history."""

    _MAXLEN = 20

    def __init__(self, output):
        self.__wrapped_output = output
        self._output_buffer = []
        self._cell_counter = 0
        self._cell_output_history = deque(maxlen=self._MAXLEN)

    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        return getattr(self.__wrapped_output, attr)

    @property
    def capture_stdout(self):
        return WrappedStdout(self._output_buffer)

    def finalize_cell(self):
        """Store the current buffered output as 1 cell output in the history."""
        if self._output_buffer:
            output = "".join(
                [x if isinstance(x, str) else str(x) for x in self._output_buffer]
            )
            output = re.sub(
                r"^(\s+Out\s\[\d+\]:\s+)", "", output, count=1, flags=re.MULTILINE
            )
            self._output_buffer.clear()
        else:
            output = None
        self._cell_output_history.append(output)
        self._cell_counter += 1

    def __getitem__(self, item: int) -> Optional[str]:
        """Note that the ptpython cell index starts counting from 1

        item > 0 will be interpreted as the cell index
        item < 0 will be interpreted as the most recent cell output (-1 is the last output)
        item == 0 raise IndexError

        The output value of a cell without output is `None`.
        """
        if not isinstance(item, int):
            raise TypeError(item)
        if item > 0:
            # convert cell index to queue index
            idx = item - self._cell_counter - 1
            if idx >= 0:
                raise IndexError(f"the last cell is OUT [{self._cell_counter}]")
        elif item == 0:
            idx_min = max(self._cell_counter - self._MAXLEN + 1, 1)
            raise IndexError(f"the first available cell is OUT [{idx_min}]")
        elif (item + self._cell_counter) < 0:
            idx_min = max(self._cell_counter - self._MAXLEN + 1, 1)
            raise IndexError(f"the first available cell is OUT [{idx_min}]")
        else:
            idx = item
        try:
            return self._cell_output_history[idx]
        except IndexError:
            idx_min = max(self._cell_counter - self._MAXLEN + 1, 1)
            raise IndexError(f"the first available cell is OUT [{idx_min}]") from None

    def write(self, data):
        self._output_buffer.append(data)
        self.__wrapped_output.write(data)

    def fileno(self):
        return self.__wrapped_output.fileno()


@functools.singledispatch
def format_repl(arg):
    """Customization point format_repl for any types that need specific
    handling. This default implementation returns the __info__ if available.

    Usage:

    from bliss.shell.cli.repl import format_repl

    @format_repl.register
    def _(arg: Foo):
        # Returns the representation of Foo
        return f"{arg.bar}"
    """
    return arg


@format_repl.register
def _(arg: HasInfo):
    """Specialization for types that implement the __info__ protocol."""

    class _InfoResult:
        def __repr__(self):
            return info(arg)

    return _InfoResult()


@format_repl.register
def _(arg: ur.Quantity):
    """Specialization for Quantity"""

    class _QuantityResult:
        def __repr__(self):
            return f"{arg:~P}"  # short pretty formatting

    return _QuantityResult()


class BlissReplBase(NoThreadPythonRepl, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        prompt_label = kwargs.pop("prompt_label", "BLISS")
        title = kwargs.pop("title", None)
        session = kwargs.pop("session")
        style = kwargs.pop("style")

        # bliss_bar = status_bar(self)
        # toolbars = list(kwargs.pop("extra_toolbars", ()))
        # kwargs["_extra_toolbars"] = [bliss_bar] + toolbars

        # Catch and remove additional kwargs
        self.session_name = kwargs.pop("session_name", "default")
        self.use_tmux = kwargs.pop("use_tmux", False)

        # patch ptpython statusbar
        if self.use_tmux and not is_windows():
            ptpython.layout.status_bar = TMUXstatus_bar
        else:
            ptpython.layout.status_bar = NEWstatus_bar

        super().__init__(*args, **kwargs)

        self.app.output = PromptToolkitOutputWrapper(self.app.output)

        if title:
            self.terminal_title = title

        # self.show_bliss_bar = True
        # self.bliss_bar = bliss_bar
        # self.bliss_bar_format = "normal"
        self.bliss_session = session
        self.bliss_prompt = BlissPrompt(self, prompt_label)
        self.all_prompt_styles["bliss"] = self.bliss_prompt
        self.prompt_style = "bliss"

        self.show_signature = True

        self.color_depth = "DEPTH_8_BIT"
        try:
            theme = style_from_pygments_cls(get_style_by_name(style))
        except ClassNotFound:
            print(
                f"Unknown color style class: {style}. using default. (check your bliss.ini)."
            )
            theme = style_from_pygments_cls(get_style_by_name("default"))

        self.install_ui_colorscheme("bliss_ui", theme)
        self.use_ui_colorscheme("bliss_ui")
        self.install_code_colorscheme("bliss_code_ui", theme)
        self.use_code_colorscheme("bliss_code_ui")

        # PTPYTHON SHELL PREFERENCES
        self.enable_history_search = True
        self.show_status_bar = True
        self.confirm_exit = True
        self.enable_mouse_support = False

        if self.use_tmux:
            self.exit_message = (
                "Do you really want to close session? (CTRL-B D to detach)"
            )

        self.typing_helper = TypingHelper(self)

    ##
    # NB: next methods are overloaded
    ##
    def eval(self, text):
        logging.getLogger("user_input").info(text)
        elogbook.command(text)
        with self.app.output.capture_stdout:
            result = super().eval(text)
            if result is None:
                # show_result will not be called
                self.app.output.finalize_cell()
            return result

    async def eval_async(self, text):
        logging.getLogger("user_input").info(text)
        elogbook.command(text)
        with self.app.output.capture_stdout:
            result = await super().eval_async(text)
            if result is None:
                # show_result will not be called
                self.app.output.finalize_cell()
            return result

    def show_result(self, result):
        """This is called when the return value of the command is not None."""
        try:
            result = format_repl(result)
        except BaseException:
            # display exception, but do not propagate and make shell to die
            sys.excepthook(*sys.exc_info())
        else:
            return super().show_result(result)
        finally:
            self.app.output.finalize_cell()

    def _handle_keyboard_interrupt(self, e: KeyboardInterrupt) -> None:
        sys.excepthook(*sys.exc_info())

    def _handle_exception(self, e):
        sys.excepthook(*sys.exc_info())


class BlissRepl(BlissReplBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._sigint_handler = gevent.signal_handler(signal.SIGINT, self._handle_ctrl_c)

    def _handle_ctrl_c(self):
        with self._lock:
            if self._current_eval_g:
                self._current_eval_g.kill(KeyboardInterrupt, block=False)


def configure_repl(repl):

    # intended to be used for testing as ctrl+t can be send via stdin.write(bytes.fromhex("14"))
    # @repl.add_key_binding(Keys.ControlT)
    # def _(event):
    #    sys.stderr.write("<<BLISS REPL TEST>>")
    #    text = repl.default_buffer.text
    #    sys.stderr.write("<<BUFFER TEST>>")
    #    sys.stderr.write(text)
    #    sys.stderr.write("<<BUFFER TEST>>")
    #    sys.stderr.write("<<HISTORY>>")
    #    sys.stderr.write(repl.default_buffer.history._loaded_strings[-1])
    #    sys.stderr.write("<<HISTORY>>")
    #    sys.stderr.write("<<BLISS REPL TEST>>")

    @repl.add_key_binding(
        Keys.ControlSpace, filter=has_focus(DEFAULT_BUFFER), eager=True
    )
    def _(event):
        """
        Initialize autocompletion at cursor.
        If the autocompletion menu is not showing, display it with the
        appropriate completions for the context.
        If the menu is showing, select the next completion.
        """

        b = event.app.current_buffer
        if b.complete_state:
            b.complete_next()
        else:
            b.start_completion(select_first=False)


def initialize(
    session_name=None, session_env=None, expert_error_report=True, early_log_info=None
) -> session_mdl.Session:
    """
    Initialize a session.

    Create a session from its name, and update a provided env dictionary.

    Arguments:
        session_name: Name of the session to load
        session_env: Dictionary containing an initial env to feed. If not defined
                     an empty dict is used
    """
    if session_env is None:
        session_env = {}

    # Add config to the user namespace
    config = static.get_config()

    """ BLISS CLI welcome messages """

    # Version
    _version = "version %s" % release.version

    # Hostname
    _hostname = platform.node()

    # Beacon host/port
    try:
        _host = get_default_connection()._host
        _port = str(get_default_connection()._port)
    except Exception:
        _host = "UNKNOWN"
        _port = "UNKNOWN"

    # Conda environment
    try:
        _env_name = os.environ["CONDA_DEFAULT_ENV"]
        _env_name = BLUE(f"{_env_name}")
        _conda_env = "(in %s Conda environment)" % _env_name
    except KeyError:
        _conda_env = ""

    print_rainbow_banner()
    print("")

    _hostname = BLUE(f"{_hostname}")
    _host = BLUE(f"{_host}")

    print(f"Welcome to BLISS {_version} running on {_hostname} {_conda_env}")
    print("Copyright (c) 2015-2022 Beamline Control Unit, ESRF")
    print("-")
    print(f"Connected to Beacon server on {_host} (port {_port})")

    if early_log_info is not None and early_log_info.count > 0:
        print()
        print(
            f"During the import {early_log_info.count} warnings were ignored. Restart BLISS with --debug to display them."
        )

    if config.invalid_yaml_files:
        print()
        print(
            f"Ignored {len(config.invalid_yaml_files)} YAML file(s) due to parsing error(s), use config.parsing_report() for details.\n"
        )

    # Setup(s)
    if session_name is None:
        session = DefaultSession()
    else:
        # we will lock the session name
        # this will prevent to start serveral bliss shell
        # with the same session name
        # lock will only be released at the end of process
        default_cnx = get_default_connection()
        try:
            default_cnx.lock(session_name, timeout=1.0)
        except RuntimeError:
            try:
                lock_dict = default_cnx.who_locked(session_name)
            except RuntimeError:  # Beacon is to old to answer
                raise RuntimeError(f"{session_name} is already started")
            else:
                raise RuntimeError(
                    f"{session_name} is already running on %s"
                    % lock_dict.get(session_name)
                )
        # set the client name to somethings useful
        try:
            default_cnx.set_client_name(
                f"host:{socket.gethostname()},pid:{os.getpid()} cmd: **bliss -s {session_name}**"
            )
        except RuntimeError:  # Beacon is too old
            pass
        session = config.get(session_name)
        print("%s: Loading config..." % session.name)

    from bliss.shell import standard

    cmds = {k: standard.__dict__[k] for k in standard.__all__}
    session_env.update(cmds)

    session_env["history"] = lambda: print("Please press F3-key to view history!")

    if session.setup(
        session_env, verbose=True, expert_error_report=expert_error_report
    ):
        print("Done.")
    else:
        print("Warning: error(s) happened during setup, setup may not be complete.")
    print("")

    log = logging.getLogger("startup")
    log.info(
        f"Started BLISS version "
        f"{_version} running on "
        f"{_hostname} "
        f"{_conda_env} "
        f"connected to Beacon server {_host}"
    )

    return session


def _archive_history(
    history_filename, file_size_thresh=10**6, keep_active_entries=1000
):
    if (
        os.path.exists(history_filename)
        and os.stat(history_filename).st_size > file_size_thresh
    ):
        with open(history_filename, "r") as f:
            lines = f.readlines()

        # history is handled as a list of entries (block of lines) to avoid splitting them while archiving
        entries = []
        entry = []
        for line in lines:
            if not line.isspace():
                entry.append(line)
            elif entry:
                entries.append(entry)
                entry = []
        if entry:
            entries.append(entry)

        now = datetime.now()
        archive_filename = f"{history_filename}_{now.year}{now.month:02}{now.day:02}"
        with open(archive_filename, "a") as f:
            for entry in entries[:-keep_active_entries]:
                f.write("".join(entry) + "\n")

        with open(history_filename, "w") as f:
            for entry in entries[-keep_active_entries:]:
                f.write("".join(entry) + "\n")


def cli(
    locals=None,
    session_name=None,
    vi_mode=False,
    startup_paths=None,
    use_tmux=False,
    expert_error_report=False,
    style="default",
    early_log_info=None,
    **kwargs,
):
    """
    Create a command line interface

    Args:
        session_name : session to initialize (default: None)
        vi_mode (bool): Use Vi instead of Emacs key bindings.
    """
    set_bliss_shell_mode(True)

    # Enable loggers
    userlogger.enable()  # destination: user
    elogbook.enable()  # destination: electronic logbook

    # user namespace
    user_ns = {}
    protected_user_ns = ProtectedDict(user_ns)

    # These 2 commands can be used by user script loaded during
    # the initialization
    user_ns["protect"] = protected_user_ns.protect
    user_ns["unprotect"] = protected_user_ns.unprotect

    if session_name and not session_name.startswith(constants.DEFAULT_SESSION_NAME):
        try:
            session = initialize(
                session_name,
                session_env=user_ns,
                expert_error_report=expert_error_report,
                early_log_info=early_log_info,
            )
        except RuntimeError as e:
            if use_tmux:
                print("\n", "*" * 20, "\n", e, "\n", "*" * 20)
                gevent.sleep(10)  # just to let the eyes to see the message ;)
            raise
    else:
        session = initialize(
            session_name=None,
            session_env=user_ns,
            expert_error_report=expert_error_report,
            early_log_info=early_log_info,
        )

    if session.name != constants.DEFAULT_SESSION_NAME:
        protected_user_ns._protect(session.object_names)
        # protect Aliases if they exist
        if "ALIASES" in protected_user_ns:
            for alias in protected_user_ns["ALIASES"].names_iter():
                if alias in protected_user_ns:
                    protected_user_ns._protect(alias)

    def last_error(index=None):
        hist = user_ns["ERROR_REPORT"].history
        try:
            idx = -1 if index is None else index
            fmt_tb = hist[idx].format(
                disable_blacklist=user_ns["ERROR_REPORT"].expert_mode,
                max_nb_locals=15,
                max_local_len=200,
            )
            pprint_traceback(fmt_tb, BlissRepl()._current_style)
        except IndexError:
            if index is None:
                print("None")
            else:
                print(f"No exception with index {index} found, size is {len(hist)}")

    # handle the last error report
    # (in the shell env only)
    user_ns["last_error"] = last_error

    # protect certain imports and Globals
    to_protect = [
        "ERROR_REPORT",
        "last_error",
        "ALIASES",
        "SCAN_DISPLAY",
        "SCAN_SAVING",
        "SCANS",
    ]
    to_protect.extend(standard.__all__)
    protected_user_ns._protect(to_protect)

    def get_globals():
        return protected_user_ns

    if session_name and not session_name.startswith(constants.DEFAULT_SESSION_NAME):
        session_id = session_name
        session_title = "Bliss shell ({0})".format(session_name)
        prompt_label = session_name.upper()
    else:
        session_id = "default"
        session_title = "Bliss shell"
        prompt_label = "BLISS"

    history_filename = ".bliss_%s_history" % (session_id)
    if is_windows():
        history_filename = os.path.join(os.environ["USERPROFILE"], history_filename)
    else:
        history_filename = os.path.join(os.environ["HOME"], history_filename)

    _archive_history(history_filename)

    # Create REPL.
    repl = BlissRepl(
        get_globals=get_globals,
        session=session,
        vi_mode=vi_mode,
        prompt_label=prompt_label,
        title=session_title,
        history_filename=history_filename,
        startup_paths=startup_paths,
        session_name=session_name,
        use_tmux=use_tmux,
        style=style,
        **kwargs,
    )

    # Custom keybindings
    configure_repl(repl)

    return repl


def embed(*args, **kwargs):
    """
    Call this to embed bliss shell at the current point in your program
    """
    with log_utils.filter_warnings():
        cmd_line_i = cli(*args, **kwargs)
        with patch_stdout_context(raw=True):
            asyncio.run(cmd_line_i.run_async())

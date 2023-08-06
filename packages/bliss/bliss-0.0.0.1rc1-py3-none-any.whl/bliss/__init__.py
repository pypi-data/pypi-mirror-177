# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Bliss main package

.. autosummary::
    :toctree:

    comm
    common
    config
    controllers
    physics
    scanning
    shell
    tango
    flint
"""
from . import release

__version__ = release.version

from bliss.common.greenlet_utils import patch_gevent as _patch_gevent

_patch_gevent()

from blissdata.client import set_default_redis_connection_manager_callback
from bliss.config.conductor.client import get_default_redis_connection_manager

set_default_redis_connection_manager_callback(get_default_redis_connection_manager)

from bliss.common.proxy import Proxy as _Proxy


def _get_current_session():
    from bliss.common import session

    return session.get_current_session()


current_session = _Proxy(_get_current_session)

from bliss.common.alias import MapWithAliases as _MapWithAliases

global_map = _MapWithAliases(current_session)
import atexit as _atexit

_atexit.register(global_map.clear)

from bliss.common.logtools import Log as _Log

# initialize the global logging
# it creates the "global" and "global.controllers" loggers
# (using BlissLoggers class with a default NullHandler handler)
# stdout_handler and beacon_handler not started here/yet
global_log = _Log(map=global_map)


# Bliss shell mode False indicates Bliss in running in library mode
_BLISS_SHELL_MODE = False


def set_bliss_shell_mode(mode=True):
    """
    Set Bliss shell mode
    """
    global _BLISS_SHELL_MODE
    _BLISS_SHELL_MODE = mode


def is_bliss_shell():
    """
    Tells if Bliss is running in shell or library mode
    """
    return _BLISS_SHELL_MODE

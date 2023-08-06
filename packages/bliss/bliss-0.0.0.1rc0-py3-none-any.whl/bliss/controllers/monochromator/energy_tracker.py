import numpy as np
import math
import xcalibu
import scipy.constants as codata
import tabulate
from datetime import datetime

from bliss.config.conductor import client
from blissdata import settings
from bliss.common.utils import (
    add_property,
    add_object_method,
    add_autocomplete_property,
    autocomplete_property,
)


class EnergyTrackingObject:
    def __init__(self, config):

        self.__mono = None
        self.__settings = None
        self.__config = config
        self.__name = config["name"]

        self.motors = {}
        self.parameters = {}
        self.def_val = {}

        self._tracking_config = self.config.get("tracking")
        for tracking in self._tracking_config:
            axis = tracking.get("motor")
            axis_name = axis.name
            self.motors[axis_name] = axis
            if "parameters" in tracking.keys():
                traj_sel = None
                self.parameters[axis_name] = {}
                mode = tracking["mode"]
                parameters = tracking.get("parameters")
                for traj_config in parameters:
                    # trajectory name is given by `harmonic` or `trajectory` key
                    traj_name = traj_config.get(
                        "harmonic", traj_config.get("trajectory")
                    )
                    if traj_sel is None:
                        traj_sel = traj_name
                    self.parameters[axis_name][traj_name] = dict()

                    # fill polynom coefficients
                    if "polynom" in traj_config:

                        for coef in ["E6", "E5", "E4", "E3", "E2", "E1", "E0"]:
                            self.parameters[axis_name][traj_name][coef] = float(
                                traj_config["polynom"][coef]
                            )

                    # fill theory coefficients
                    if "theory" in traj_config:

                        for coef in ["TG0", "TL0", "TGAM", "TB0"]:
                            self.parameters[axis_name][traj_name][coef] = float(
                                traj_config["theory"][coef]
                            )

                    # calibration table
                    if "table" in traj_config:
                        self.parameters[axis_name][traj_name][
                            "calib_file"
                        ] = traj_config["table"]
                        self.read_calib(axis, traj_name)

                    # check parameter consistency with current mode
                    # if len(self.parameters[axis_name][traj_name].keys()) == 0:
                    #     raise RuntimeError("missing parameters in config")
                    if mode == "table":
                        if "table" not in traj_config:
                            raise RuntimeError("missing 'table' parameter in config")
                    elif mode == "polynom":
                        if not all(
                            e in traj_config["polynom"]
                            for e in ["E0", "E1", "E2", "E3", "E4", "E5", "E6"]
                        ):
                            raise RuntimeError(
                                "missing polynom coefficient in [E0, E1, E2, E3, E4, E5, E6]"
                            )
                    elif mode == "theory":
                        if not all(
                            e in traj_config["theory"]
                            for e in ["TG0", "TL0", "TGAM", "TB0"]
                        ):
                            raise RuntimeError(
                                "missing theory coefficient in [TG0, TL0, TGAM, TB0]"
                            )
                    else:
                        raise RuntimeError(
                            "invalid mode not in [polynom, table, theory]"
                        )

                self.def_val[axis_name] = {
                    "trajectory": traj_sel,
                    "track": True,
                    "mode": mode,
                    "track_offset": 0.0,
                }
        self.__settings_name = f"{self.name}_track_setting"
        self.__settings = settings.HashObjSetting(
            self.__settings_name, default_values=self.def_val
        )

        for axis in self.motors.values():
            # set tracking properties
            setattr(axis, "tracker", self)
            add_object_method(axis, self.track_info, None)
            add_property(
                axis,
                "track",
                lambda self: self.tracker._track(self),
                lambda self, state: self.tracker._track(self, state),
            )
            add_property(
                axis,
                "harmonic",
                lambda self: self.tracker.harmonic(self),
                lambda self, harmonic: self.tracker.harmonic(self, harmonic),
            )
            add_property(
                axis,
                "trajectory",
                lambda self: self.tracker.trajectory(self),
                lambda self, trajectory: self.tracker.trajectory(self, trajectory),
            )
            add_property(
                axis,
                "track_mode",
                lambda self: self.tracker.track_mode(self),
                lambda self, mode: self.tracker.track_mode(self, mode),
            )
            add_property(
                axis,
                "track_offset",
                lambda self: self.tracker.track_offset(self),
                lambda self, offset: self.tracker.track_offset(self, offset),
            )
            add_autocomplete_property(
                axis, "track_table", lambda self: self.tracker.track_table(self)
            )

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

    @property
    def settings(self):
        return self.__settings

    @property
    def mono(self):
        return self.__mono

    @mono.setter
    def mono(self, mono):
        self.__mono = mono

    def __info__(self):
        motors = self.mono.motors
        bragg = motors["bragg"].position
        energy = self.mono.bragg2energy(bragg)

        #
        # TITLE
        #
        title = [""]
        for axis in self.motors.values():
            title.append(axis.name)

        #
        # CALCULATED POSITION ROW
        #
        calculated = ["Calculated"]
        for axis in self.motors.values():
            track = self.energy2tracker(axis, energy)
            calculated.append(f"{track:.3f} {axis.unit}")

        #
        # CURRENT POSITION ROW
        #
        current = ["Current"]
        for axis in self.motors.values():
            current.append(f"{axis.position:.3f} {axis.unit}")

        #
        # TRACKING ROW
        #
        tracking = ["Tracking"]
        for axis in self.motors.values():
            tracking.append("ON" if axis.track else "OFF")

        mystr = tabulate.tabulate(
            [calculated, current, tracking],
            headers=title,
            tablefmt="plain",
            stralign="right",
        )

        return mystr

    def _track(self, axis, state=None):
        if state is not None:
            setting = self.settings[axis.name]
            setting["track"] = state
            self.settings[axis.name] = setting
        return self.settings[axis.name]["track"]

    def track_info(self, *axes):
        """Display tracking info"""
        if len(axes) == 0:
            axes = self.motors.values()
        else:
            axes = [axis for axis in axes if axis in self.motors.values()]

        motors = self.mono.motors
        bragg = motors["bragg"].position
        energy = self.mono.bragg2energy(bragg)

        #
        # TITLE
        #
        title = [""]
        for axis in axes:
            title.append(axis.name)

        #
        # TRACKING MODE ROW
        #
        track_mode = ["Mode"]
        for axis in axes:
            track_mode.append(axis.track_mode)

        #
        # TRAJECTORY ROW
        #
        track_traj = ["Trajectory"]
        for axis in axes:
            track_traj.append(axis.trajectory)

        #
        # TRACKING ROW
        #
        tracking = ["Tracking"]
        for axis in axes:
            tracking.append("ON" if axis.track else "OFF")

        #
        # On Trajectory row
        #
        ontraj = ["On traj."]
        for axis in axes:
            is_on_traj = math.isclose(
                axis.position, self.energy2tracker(axis, energy), abs_tol=0.0005
            )
            ontraj.append("YES" if is_on_traj else "NO")

        mystr = tabulate.tabulate(
            [tracking, track_mode, track_traj, ontraj],
            headers=title,
            tablefmt="plain",
            stralign="right",
        )

        print(f"\n{mystr}\n")

    def track_on(self, *axes):
        """Enable tracking for all or given motors in this tracker"""
        if len(axes) == 0:
            axes = self.motors.values()
        else:
            axes = [axis for axis in axes if axis in self.motors.values()]
        for mot in axes:
            mot.track = True

    def track_off(self, *axes):
        """Disable tracking for all or given motors in this tracker"""
        if len(axes) == 0:
            axes = self.motors.values()
        else:
            axes = [axis for axis in axes if axis in self.motors.values()]
        for mot in axes:
            mot.track = False

    def harmonic(self, axis, harmonic=None):
        if harmonic is not None and harmonic not in self.parameters[axis.name].keys():
            raise ValueError(f"harmonic {harmonic} does not exist in parameters")
        return self.trajectory(axis, harmonic)

    def trajectory(self, axis, traj=None):
        if traj is not None:
            if traj not in self.parameters[axis.name].keys():
                raise ValueError(f"trajectory {traj} does not exist in parameters")
            setting = self.settings[axis.name]
            setting["trajectory"] = traj
            self.settings[axis.name] = setting
        return self.settings[axis.name]["trajectory"]

    def track_mode(self, axis, mode=None):
        if mode is not None:
            if mode in ("polynom", "table", "theory"):
                setting = self.settings[axis.name]
                setting["mode"] = mode
                self.settings[axis.name] = setting
            else:
                raise ValueError(f"mode {mode} does not exist (polynom, table, theory)")
        return self.settings[axis.name]["mode"]

    def track_offset(self, axis, offset=None):
        if offset is not None:
            setting = self.settings[axis.name]
            setting["track_offset"] = offset
            self.settings[axis.name] = setting
        return self.settings[axis.name]["track_offset"]

    def track_table(self, axis):
        return self.parameters[axis.name][axis.trajectory]["calib"]

    #
    # Table
    #
    def read_calib(self, axis, traj):
        calib_file = self.parameters[axis.name][traj]["calib_file"]
        tmp_calib_file = f"/tmp/tmp_calib_file_{axis.name}"

        with open(tmp_calib_file, "w") as xcalib:
            content = client.get_config_file(calib_file).decode("utf-8")
            xcalib.write(content)

        calib = xcalibu.Xcalibu()
        calib.set_calib_name(axis.name)
        calib.set_calib_time(0)
        calib.set_calib_file_name(tmp_calib_file)
        calib.set_calib_type("TABLE")
        calib.set_reconstruction_method("INTERPOLATION")
        calib.load_calib()

        self.parameters[axis.name][traj]["calib"] = TrackTable(
            axis, calib=calib, filename=calib_file
        )

    def get_track_from_table(self, axis_name, traj, energy):

        e_min = self.parameters[axis_name][traj]["calib"].calib.min_x()
        e_max = self.parameters[axis_name][traj]["calib"].calib.max_x()

        if isinstance(energy, np.ndarray):
            ene = np.copy(energy)
        else:
            ene = np.array([energy], dtype=float)

        track = np.copy(ene)
        for i in range(ene.size):
            if ene[i] >= e_min and ene[i] <= e_max:
                track[i] = self.parameters[axis_name][traj]["calib"].calib.get_y(ene[i])
            else:
                # XXX what to do in this case ? polynom may not be defined
                track[i] = np.nan
                # track[i] = self.get_track_from_polynom(axis_name, traj, ene[i])

        if track.size == 1:
            return track[0]

        return track

    #
    # Polynom
    #
    def get_track_from_polynom(self, axis_name, traj, energy):
        track = (
            self.parameters[axis_name][traj]["E6"] * np.power(energy, 6)
            + self.parameters[axis_name][traj]["E5"] * np.power(energy, 5)
            + self.parameters[axis_name][traj]["E4"] * np.power(energy, 4)
            + self.parameters[axis_name][traj]["E3"] * np.power(energy, 3)
            + self.parameters[axis_name][traj]["E2"] * np.power(energy, 2)
            + self.parameters[axis_name][traj]["E1"] * np.power(energy, 1)
            + self.parameters[axis_name][traj]["E0"]
        )
        return track

    #
    # Theory
    #
    def get_track_from_theory(self, axis_name, harmonic, energy):
        # the following has to be changed to be consistent with the rest of bliss
        hc_over_e = (
            codata.Planck * codata.speed_of_light / codata.elementary_charge * 1e7
        )

        gap_off = self.parameters[axis_name][harmonic]["TG0"]
        lambda_0 = self.parameters[axis_name][harmonic]["TL0"]
        gamma_machine = self.parameters[axis_name][harmonic]["TGAM"]
        B_0 = self.parameters[axis_name][harmonic]["TB0"]
        K = (
            codata.elementary_charge
            / (2 * np.pi * codata.electron_mass * codata.speed_of_light)
            * 1e-3
            * B_0
            * lambda_0
        )
        # print('K',K)
        wavelength = hc_over_e / energy
        # print('lambda',wavelengths)
        k = np.sqrt(4e-7 * harmonic * wavelength / lambda_0 * gamma_machine**2 - 2)
        # print('k',k)
        track = gap_off - lambda_0 / np.pi * np.log(k / K)
        return track

    def get_energy_from_theory(self, axis_name, harmonic, gap):
        # the following has to be changed to be consistent with the rest of bliss
        hc_over_e = (
            codata.Planck * codata.speed_of_light / codata.elementary_charge * 1e7
        )

        gap_off = self.parameters[axis_name][harmonic]["TG0"]
        lambda_0 = self.parameters[axis_name][harmonic]["TL0"]
        gamma_machine = self.parameters[axis_name][harmonic]["TGAM"]
        B_0 = self.parameters[axis_name][harmonic]["TB0"]
        K = (
            codata.elementary_charge
            / (2 * np.pi * codata.electron_mass * codata.speed_of_light)
            * 1e-3
            * B_0
            * lambda_0
        )
        wavelength = (
            lambda_0
            / (4e-7 * harmonic * gamma_machine**2)
            * (K**2 * np.exp(2 * np.pi * (gap_off - gap) / lambda_0) + 2)
        )
        # print(wavelength)
        ene = hc_over_e / wavelength
        return ene

    def energy2tracker(self, axis, energy):
        traj_sel = self.settings[axis.name]["trajectory"]
        track_offset = self.settings[axis.name]["track_offset"]

        if traj_sel is None:
            raise RuntimeError(f"{axis.name}: No harmonic/trajectory selected")
        if traj_sel not in self.parameters[axis.name].keys():
            raise RuntimeError(
                f"Harmonic/trajectory {traj_sel} does not exist for {axis.name}"
            )

        track = np.nan
        mode = self.settings[axis.name]["mode"]
        if mode == "polynom":
            track = (
                self.get_track_from_polynom(axis.name, traj_sel, energy) + track_offset
            )
        if mode == "table":
            track = (
                self.get_track_from_table(axis.name, traj_sel, energy) + track_offset
            )
        if mode == "theory":
            track = (
                self.get_track_from_theory(axis.name, traj_sel, energy) + track_offset
            )

        return track

    def tracker2energy(self, axis, gap):
        # currently implemented only for "theory" mode
        # must be somehow possible for others, I will try to think of it (BD)
        traj_sel = self.settings[axis.name]["trajectory"]
        track_offset = self.settings[axis.name]["track_offset"]

        if traj_sel is None:
            raise RuntimeError(f"{axis.name}: No harmonic/trajectory selected")
        if traj_sel not in self.parameters[axis.name].keys():
            raise RuntimeError(f"Harmonic {traj_sel} does not exist for {axis.name}")

        ene = np.nan  # why? but I will do the same (BD)
        mode = self.settings[axis.name]["mode"]
        if mode == "polynom":
            raise NotImplementedError
        if mode == "table":
            raise NotImplementedError
        if mode == "theory":
            ene = self.get_energy_from_theory(axis.name, traj_sel, gap - track_offset)

        return ene


class TrackTable:
    def __init__(self, axis, calib=None, filename=None, kev_tolerance=0.01):
        self.__calib = calib
        self._filename = filename
        self._axis = axis
        self._kev_tolerance = kev_tolerance
        self._backup = True

    @autocomplete_property
    def calib(self):
        return self.__calib

    @calib.setter
    def calib(self, calib):
        self.__calib = calib

    def save(self):
        """Save table calib file to beamline configuration"""
        if self._backup:
            # suffix current file with the date of the day
            content = client.get_config_file(self._filename).decode("utf-8")
            today = datetime.today().strftime("%Y%m%d")
            client.set_config_db_file(f"{self._filename}.{today}", content)

        self.calib.save()
        with open(self.calib.get_calib_file_name(), "r") as calib_file:
            content = calib_file.read()
        client.set_config_db_file(self._filename, content)

    def plot(self):
        """Display table points on a plot"""
        return self.calib.plot()

    def __info__(self):
        """Print table points (energy, motor position)"""
        title = ["Energy", self._axis.name]
        data = zip(self.calib.x_raw, self.calib.y_raw)
        mystr = tabulate.tabulate(data, headers=title)
        return f"File: {self._filename}\n\n{mystr}"

    def _energy_in_table(self, energy):
        """Check if energy is in table with given tolerance"""
        return np.any(
            np.isclose(energy, self.calib.get_raw_x(), atol=self._kev_tolerance)
        )

    def setpoint(self):
        """Add current position (energy, motor) to table"""
        current_energy = round(self._axis.tracker.mono.energy_motor.position, 6)
        if self._energy_in_table(current_energy):
            self.calib.delete(x=current_energy)
        self.calib.insert(x=current_energy, y=self._axis.position)

    def delpoint(self, energy=None):
        """Delete current energy from table"""
        if energy is None:
            energy = round(self._axis.tracker.mono.energy_motor.position, 6)
        self.calib.delete(x=energy)

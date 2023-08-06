# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""
Definition of classes representing a set of common functionalities for
monochromator control.

We assume that a monochromator is composed of:
    - Rotation motor (bragg angle - real motor)
    - Energy motor (Calc Motor)
    - Crystal(s)

The corresponding classes are MonochromatorBase, XtalManager and EnergyCalcMotor.
Configuration examples can be found in:
https://bliss.gitlab-pages.esrf.fr/bliss/master/config_mono.html
"""

import math
import functools
import copy
import numpy as np
import xcalibu
import tabulate
import abc

from bliss.common.types import IterableNamespace
from bliss.common.utils import autocomplete_property
from bliss.common.logtools import log_error
from bliss.common.axis import Axis
from bliss.common.protocols import HasMetadataForDataset, HasMetadataForScan

from blissdata import settings
from bliss.physics.units import ur, units
from bliss.physics.diffraction import CrystalPlane, _get_all_crystals, MultiPlane, hc
from bliss.controllers.bliss_controller import BlissController
from bliss.controllers.monochromator.monochromator_calcmotor import (
    EnergyCalcMotor,
    EnergyTrackingCalcMotor,
    BraggFixExitCalcMotor,
)


class MonochromatorBase(
    BlissController, HasMetadataForScan, HasMetadataForDataset, metaclass=abc.ABCMeta
):
    """
    Monochromator Base
    """

    def __init__(self, config):

        super().__init__(config)
        self.__settings = None
        self._enecc = None
        self._enetrackcc = None

        self._trackers = self.config.get("trackers")
        # tracking objects
        if self._trackers:
            trackers = {tracker.name: tracker for tracker in self._trackers}
            for tracker in trackers.values():
                tracker.mono = self
            self._trackers = trackers

        # bragg motor
        assert self.bragg_motor.unit, "Please specify unit for the Bragg motor"

        self.track_tables = TrackTableMulti(lambda: self.tracked_axes)

    def _get_item_owner(self, name, cfg, pkey):
        if pkey == "energy_motor":
            if self._enecc is None:
                # Energy Calc Motor config is like:
                #
                # - plugin: emotion
                #   module: monochromator
                #   class: EnergyCalcMotor
                #   axes:
                #     - name: $sim_mono
                #       tags: real bragg
                #     - name: ene
                #       tags: energy
                #       unit: keV
                conf = {
                    "axes": [
                        {"name": self.bragg_motor, "tags": "real bragg"},
                        {
                            "name": cfg["name"],
                            "tags": "energy",
                            "unit": cfg.get("unit"),
                        },
                    ]
                }

                self._enecc = EnergyCalcMotor("enecc", conf)
                self._enecc._initialize_config()
                self._enecc.set_mono(self)
            return self._enecc
        if pkey == "energy_track_motor":
            if self._enetrackcc is None:
                # EnergyTrack CalcMotor config is like:
                #
                # - plugin: emotion
                #   module: monochromator
                #   class: EnergyTrackingCalcMotor
                #   approximation: 0.0005
                #   axes:
                #     - name: $ene
                #       tags: real energy
                #     - name: $sim_c1
                #       tags: real sim_c1
                #     - name: $sim_c2
                #       tags: real sim_c2
                #     - name: $sim_acc
                #       tags: real sim_acc
                #     - name: enetrack
                #       tags: energy_track
                #       unit: keV
                conf = {
                    "axes": [
                        {"name": self.energy_motor, "tags": "real energy"},
                        {
                            "name": cfg["name"],
                            "tags": "energy_track",
                            "unit": cfg.get("unit"),
                        },
                    ]
                }

                for tracker in self.trackers:
                    for axis in tracker.motors.values():
                        real = {"name": axis, "tags": "real " + axis.name}
                        conf["axes"].append(real)

                self._enetrackcc = EnergyTrackingCalcMotor("enetrackcc", conf)
                self._enetrackcc._initialize_config()
                self._enetrackcc.set_mono(self)

            return self._enetrackcc

    @autocomplete_property
    def bragg_motor(self):
        return self.config.get("bragg_motor")

    @autocomplete_property
    def energy_motor(self):
        return self._enecc.get_axis(self.config["energy_motor"]["name"])

    @autocomplete_property
    def energy_track_motor(self):
        # energy track controller can be None if there is no energy tracking
        if self._enetrackcc is not None:
            return self._enetrackcc.get_axis(self.config["energy_track_motor"]["name"])

    @autocomplete_property
    def motors(self):
        return IterableNamespace(**self._motors_dict)

    @autocomplete_property
    def trackers(self):
        return IterableNamespace(**self._trackers)

    @property
    def _motors_dict(self):
        motors = {"bragg": self.bragg_motor, "energy": self.energy_motor}
        ene_track_motor = self.energy_track_motor
        if ene_track_motor:
            motors["energy_track_motor"] = ene_track_motor
        return motors

    def _load_config(self):
        # xtals
        self.xtals = self.config.get("xtals", None)
        if self.xtals is None:
            raise RuntimeError("No XtalManager configured")
        if len(self.xtals.xtal_names) == 0:
            raise RuntimeError("No Crystals Defined in the XtalManager")

        # Add label-named method for all positions.
        for xtal in self.xtals.xtal_names:
            self._add_label_move_method(xtal)

    def _init(self):
        xtal = self.xtals.xtal_sel
        if xtal is not None:
            if not self.xtal_is_in(xtal):
                xtal_in = self.xtal_in()
                if len(xtal_in) == 0:
                    self.xtals.xtal_sel = None
                else:
                    self.xtals.xtal_sel = xtal_in[0]
        else:
            for xtal in self.xtals.xtal_names:
                if self.xtal_is_in(xtal):
                    self.xtals.xtal_sel = xtal

    def close(self):
        self.__close__()

    def __close__(self):
        for controller in filter(None, (self._enecc, self._enetrackcc)):
            controller.close()

    @property
    def settings(self):
        return self.__settings

    def __info__(self):
        info_str = self._info_mono()
        info_str += self._info_xtals()
        motors_title, calculated_motors, current_motors = self._info_motor()
        info_str += "\n" + tabulate.tabulate(
            [calculated_motors, current_motors],
            headers=motors_title,
            tablefmt="plain",
            stralign="right",
        )
        if self._trackers:
            info_str += self._info_trackers()
        return info_str

    def _info_mono(self):
        """Get the monochromator information."""
        info_str = f"Monochromator: {self.name}\n\n"
        return info_str

    def _info_xtals(self):
        """Get the christal information."""
        info_str = ""
        if not self.xtals:
            return info_str
        unit = self.bragg_motor.unit
        info_str += self.xtals.__info__()
        if unit == "deg":
            return info_str

        # there is a need to change the units and the numbers for the bragg
        bragg_index = info_str.find("Bragg")
        if bragg_index != -1:
            min_th, max_th = self.xtals.bragg_min_max(unit)
            new_str = f"Bragg [{unit}]: {max_th:.4f} - {min_th:.4f}\n"
            info_str = info_str.replace(info_str[bragg_index:], new_str)

        return info_str

    def _info_trackers(self):
        info_str = ""
        for tracker in self.trackers:
            info_str += f"\n\n{tracker.name.upper()}\n"
            info_str += tracker.__info__()
        return info_str

    def _info_motor(self):
        bragg = self.bragg_motor.position
        unit = self.bragg_motor.unit or "deg"
        value = (bragg * ur.parse_units(unit)).to("deg").magnitude
        energy = self.bragg2energy(value)
        #
        # TITLE
        #
        title = [""]
        title.append(self.bragg_motor.name)
        title.append(self.energy_motor.name)
        if self.energy_track_motor is not None:
            title.append(self.energy_track_motor.name)

        #
        # CALCULATED POSITION ROW
        #
        calculated = ["Calculated"]
        # bragg
        val = self.bragg_motor.position
        valu = self.bragg_motor.unit
        calculated.append(f"{val:.3f} {valu}")
        # energy
        valu = self.energy_motor.unit
        calculated.append(f"{energy:.3f} {valu}")
        # tracker
        if self.energy_track_motor is not None:
            valu = self.energy_track_motor.unit
            calculated.append(f"{energy:.3f} {valu}")

        #
        # CURRENT POSITION ROW
        #
        current = ["Current"]
        # bragg
        val = self.bragg_motor.position
        valu = self.bragg_motor.unit
        current.append(f"{val:.3f} {valu}")
        # energy
        valu = self.energy_motor.unit
        val = self.energy_motor.position
        current.append(f"{val:.3f} {valu}")
        # tracker
        if self.energy_track_motor is not None:
            val = self.energy_track_motor.position
            valu = self.energy_track_motor.unit
            current.append(f"{val:.3f} {valu}")

        return title, calculated, current

    """
    For SPEC compatibility:
    This method change the offset of the Bragg motor to fit with an energy
    which has been positioned using a known sample.
    Remarks:
        - The mono need to be at the given energy.
        - In case of the bragg motor being a CalcMotor, do not forget
          to foresee the set offset method in it.
    """

    def setE(self, energy):
        new_bragg_pos = self.energy2bragg(energy)
        mot = self.bragg_motor
        mot.position = new_bragg_pos
        self.energy_motor.update_position()

    ###############################################################
    ###
    ### Xtals
    ###
    @property
    def xtal_sel(self):
        return self.xtals.xtal_sel

    @xtal_sel.setter
    def xtal_sel(self, xtal):
        self.xtals.xtal_sel = xtal

    """
    In case of monochromator with multi crystals a changer may be implemented
    By default, each crystal is considered in place. Changing the crystal only
    change the energy calculation
    """

    def xtal_is_in(self, xtal):
        if xtal in self.xtals.xtal_names:
            return self._xtal_is_in(xtal)
        raise RuntimeError(f"Crystal {xtal} not configured")

    def _xtal_is_in(self, xtal):
        """
        This method needs to be overwritten to reflect the monochromator behaviour
        """
        return True

    def _add_label_move_method(self, xtal_name):
        """Add a method named after the xrtal najme to move to the
        corresponding position.
        Args:
        xtal_name (str): Chrystal or layer name.
        """

        def label_move_func(pos):
            print(f"Moving to: {pos}")
            self.xtal_change(pos)

        # name should not start with a number!
        if xtal_name.isidentifier():
            setattr(self, xtal_name, functools.partial(label_move_func, pos=xtal_name))
        else:
            log_error(
                self, f"{self.name}: '{xtal_name}' is not a valid python identifier."
            )

    def xtal_change(self, xtal):
        if xtal in self.xtals.xtal_names:
            self._xtal_change(xtal)
            self.xtals.xtal_sel = xtal
            self.energy_motor.sync_hard()
        else:
            raise RuntimeError(f"Crystal {xtal} not configured")

    @abc.abstractmethod
    def _xtal_change(self, xtal):
        """
        To be overloaded to reflect the monochromator behaviour
        """
        raise NotImplementedError

    def xtal_in(self):
        """
        return the list of crystals in place
        """
        xtal_in_place = []
        for xtal in self.xtals.xtal_names:
            if self.xtal_is_in(xtal):
                xtal_in_place.append(xtal)
        return xtal_in_place

    ################################################################
    ###
    ### Calculation methods
    ###
    def energy2bragg(self, ene):
        return self.xtals.energy2bragg(ene)

    def bragg2energy(self, bragg):
        return self.xtals.bragg2energy(bragg)

    ################################################################
    ###
    ### Tracking
    ###
    def track_info(self):
        if self.tracked_axes is None:
            print("No Tracking defined for this monochromator")
            return

        print("")

        for tracker in self.trackers:
            print(f"  {tracker.name.upper()}")
            tracker.track_info()

    def track_on(self, *axes):
        if self.energy_track_motor is None:
            raise ValueError("No Tracking defined for this monochromator")
        for tracker in self.trackers:
            tracker.track_on(*axes)

    def track_off(self, *axes):
        if self.energy_track_motor is None:
            raise ValueError("No Tracking defined for this monochromator")
        for tracker in self.trackers:
            tracker.track_off(*axes)

    # def is_tracked(self, axis):
    #     if self.energy_track_motor is None:
    #         raise ValueError("No Tracking defined for this monochromator")

    #     cont = self.energy_track_motor.controller
    #     if axis in cont.reals:
    #         tag = cont._axis_tag(axis)
    #         if tag != "energy":
    #             return axis.track

    @property
    def tracked_axes(self):
        if self.energy_track_motor is None:
            return None

        cont = self.energy_track_motor.controller
        tracked_list = []
        for axis in cont.reals:
            tag = cont._axis_tag(axis)
            if tag != "energy" and axis.track:
                tracked_list.append(axis)
        return tracked_list

    def track_mode(self, axis, mode=None):
        if self.energy_track_motor is not None:
            cont = self.energy_track_motor.controller
            if axis in cont.reals:
                tag = cont._axis_tag(axis)
                if tag != "energy":
                    if mode is None:
                        return axis.track_mode
                    axis.track_mode = mode

    def dataset_metadata(self) -> dict:
        mdata = {"name": self.name}
        xtal = self.xtal_sel
        if xtal is None:
            return mdata
        theta = self.bragg_motor.position
        unit = self.bragg_motor.unit or "deg"
        theta = theta * ur.parse_units(unit)
        mdata.update(self.xtals.get_metadata(theta))
        return mdata

    def scan_metadata(self) -> dict:
        mdata = self.dataset_metadata()
        mdata.pop("name")
        mdata["@NX_class"] = "NXmonochromator"
        if "energy" in mdata:
            mdata["energy@units"] = "keV"
        if "wavelength" in mdata:
            mdata["wavelength@units"] = "m"
        crystal = mdata.get("crystal")
        if crystal:
            crystal["@NX_class"] = "NXcrystal"
            crystal["d_spacing@units"] = "m"
        return mdata


class SimulationMonochromator(MonochromatorBase):
    """Monochromator to use for simulation or tests

    Implements required abstractions
    """

    def _xtal_change(self, xtal):
        pass


class MonochromatorFixExitBase(MonochromatorBase):
    def __init__(self, config):
        super().__init__(config)
        self._braggfecc = None

        assert (
            config.get("bragg_fe_motor") is not None
        ), "Fix exit configuration needs a 'bragg_fe_motor' section"
        assert (
            config["bragg_fe_motor"].get("unit") is not None
        ), "Fix exit Bragg FE motor needs unit"
        assert isinstance(
            self.xtal_motor, Axis
        ), "Fix exit motor configuration needs an 'xtal' key referencing a motor"

        # Fix exit Geometry
        self.__fix_exit_offset = self.config.get("fix_exit_offset", None)
        assert (
            self.fix_exit_offset is not None
        ), f"Monochromator {self.name} does not define fix_exit_offset"

    @property
    def xtal_motor(self):
        return self.config["bragg_fe_motor"].get("xtal_motor")

    @property
    def bragg_fe_motor(self):
        return self._braggfecc.get_axis(self.config["bragg_fe_motor"]["name"])

    @property
    def _motors_dict(self):
        motors = super()._motors_dict
        motors["xtal"] = self.xtal_motor
        motors["bragg_fe"] = self.bragg_fe_motor
        return motors

    def _get_item_owner(self, name, cfg, pkey):
        if pkey == "bragg_fe_motor":
            if self._braggfecc is None:
                # CalcMotor which manage Real Bragg axis and Xtal motor
                conf = {
                    "axes": [
                        {"name": self.xtal_motor, "tags": "real xtal"},
                        {"name": self.bragg_motor, "tags": "real bragg"},
                        {
                            "name": cfg["name"],
                            "tags": "bragg_fix_exit",
                            "unit": cfg["unit"],
                        },
                    ]
                }

                self._braggfecc = BraggFixExitCalcMotor("braggfecc", conf)
                self._braggfecc._initialize_config()
                self._braggfecc.set_mono(self)
            return self._braggfecc
        return super()._get_item_owner(name, cfg, pkey)

    def __close__(self):
        if self._braggfecc is not None:
            self._braggfecc.close()
        super().__close__()

    def _info_xtals(self):
        info_str = super()._info_xtals()
        info_str += f"Fix exit_offset: {self.fix_exit_offset}\n\n"
        return info_str

    def _info_motor(self):
        title, calculated, current = super()._info_motor()
        title.insert(2, self.bragg_fe_motor.name)
        calculated.insert(
            2, f"{self.bragg_fe_motor.position:.3f} {self.bragg_fe_motor.unit}"
        )
        current.insert(
            2, f"{self.bragg_fe_motor.position:.3f} {self.bragg_fe_motor.unit}"
        )
        return title, calculated, current

    @property
    def fix_exit_offset(self):
        return self.__fix_exit_offset

    @fix_exit_offset.setter
    def fix_exit_offset(self, val):
        self.__fix_exit_offset = val

    def bragg2dxtal(self, bragg):
        """
        Double Xtal Fix Exit Monochromator specific
        """
        if self.fix_exit_offset is not None:
            dxtal = self.fix_exit_offset / (2.0 * np.cos(np.radians(bragg)))
            return dxtal
        raise RuntimeError("No Fix Exit Offset defined")

    def dxtal2bragg(self, dxtal):
        if self.fix_exit_offset is not None:
            bragg = np.degrees(np.arccos(self.fix_exit_offset / (2.0 * dxtal)))
            return bragg
        raise RuntimeError("No Fix Exit Offset defined")

    def energy2dxtal(self, ene):
        bragg = self.energy2bragg(ene)
        dxtal = self.bragg2dxtal(bragg)
        return dxtal

    @abc.abstractmethod
    def dxtal2xtal(self, dxtal):
        raise NotImplementedError

    @abc.abstractmethod
    def xtal2dxtal(self, xtal):
        raise NotImplementedError

    def bragg2xtal(self, bragg):
        dxtal = self.bragg2dxtal(bragg)
        xtal = self.dxtal2xtal(dxtal)
        return xtal

    def xtal2bragg(self, xtal):
        dxtal = self.xtal2dxtal(xtal)
        bragg = self.dxtal2bragg(dxtal)
        return bragg

    def energy2xtal(self, ene):
        bragg = self.energy2bragg(ene)
        dxtal = self.bragg2dxtal(bragg)
        xtal = self.dxtal2xtal(dxtal)
        return xtal


"""
    Crystals management + Energy Calculation

    YML file example
        - plugin: bliss
          package: bm23.MONO.BM23monochromator
          class: XtalManager
          name: mono_xtals
          xtals:
            - xtal: Si111
            - xtal: Si333
            - xtal: Ge311

"""


class SimulationMonochromatorFixExit(MonochromatorFixExitBase):
    def _xtal_change(self, xtal):
        pass

    def dxtal2xtal(self, dxtal):
        return dxtal - 30

    def xtal2dxtal(self, xtal):
        return xtal + 30


class XtalManager:
    def __init__(self, config):

        self.__config = config
        self.__name = config["name"]

        # Crystal(s) management
        self.all_xtals = self.get_all_xtals()
        xtals = self.config.get("xtals")

        self.xtal_names = []
        self.xtal = {}
        for elem in xtals:
            if "xtal" in elem.keys():
                xtal_name = elem.get("xtal")
                dspacing = elem.get("dspacing", None)
                symbol = self.xtalplane2symbol(xtal_name)
                if symbol not in self.all_xtals:
                    if dspacing is not None:
                        self.xtal[xtal_name] = MultiPlane(distance=dspacing * 1e-10)
                    else:
                        raise RuntimeError("dspacing of Unknown crystals must be given")
                else:
                    self.xtal[xtal_name] = copy.copy(CrystalPlane.fromstring(xtal_name))
                if dspacing is not None:
                    self.xtal[xtal_name].d = dspacing * 1e-10
                self.xtal_names.append(xtal_name)
            elif "multilayer" in elem.keys():
                ml_name = elem.get("multilayer")
                elem["name"] = ml_name
                self.xtal[ml_name] = Multilayer(elem)
                self.xtal_names.append(ml_name)

        def_val = {"xtal_sel": None}
        self.__settings_name = f"XtalManager_{self.name}"
        self.__settings = settings.HashSetting(
            self.__settings_name, default_values=def_val
        )
        if self.settings["xtal_sel"] not in self.xtal_names:
            self.settings["xtal_sel"] = None

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
    def xtal_sel(self):
        return self.settings["xtal_sel"]

    @xtal_sel.setter
    def xtal_sel(self, xtal):
        if xtal is None or xtal in self.xtal_names:
            self.settings["xtal_sel"] = xtal
        else:
            raise RuntimeError(f"Crystal ({xtal}) not configured")

    def __info__(self):
        if self.xtal_sel is not None:
            xtal_sel = self.xtal[self.xtal_sel]
            if isinstance(xtal_sel, Multilayer):
                info_str = "Multilayer:"
            else:
                info_str = "Crystal:"
        else:
            info_str = "Crystal:"
        info_str += f" {self.xtal_sel} ("
        for xtal in self.xtal_names:
            info_str += f"{xtal} / "
        info_str = info_str[:-3] + ")"
        info_str += "\n"

        if self.xtal_sel is not None:
            if isinstance(xtal_sel, Multilayer):
                ml_str = xtal_sel.__info__()
                info_str += ml_str
            else:
                dspacing = (self.xtal[self.xtal_sel].d * ur.m).to("angstrom")
                info_str += f"dspacing: {dspacing:.5f}\n"

        return info_str

    #
    # Utils
    #

    def get_all_xtals(self):
        xtals = _get_all_crystals()
        all_xtals = []
        for xtal in xtals:
            all_xtals.append(xtal.name)
        return all_xtals

    def xtalplane2symbol(self, xtalplane):
        symbol, plane = "", ""
        for c in xtalplane:
            if c.isdigit() or c.isspace():
                plane += c
            elif c.isalpha():
                symbol += c
        return symbol

    def get_xtals_config(self, key):
        res = {}
        xtals = self.config.get("xtals")
        for elem in xtals:
            if "xtal" in elem.keys():
                elem_name = elem.get("xtal")
            elif "multilayer" in elem.keys():
                elem_name = elem.get("multilayer")
            else:
                raise RuntimeError('Neither "xtal" nor "multilayer" keyword in xtal')
            res[elem_name] = float(elem.get(key))

        return res

    def bragg_min_max(self, unit="deg"):
        """Get the theoretical min and max bragg angle values.
        Args:
            unit(str): The unit of the value as string ("deg", "mrad", "rad").
                       Default value: "deg"
        Returns:
             (tupple): The min and max theoretical value [unit]
        """
        return self.xtal[self.xtal_sel].bragg_min_max(unit)

    #
    # Calculation methods
    #

    def energy2bragg(self, ene):
        """Calculate the bragg angle as function of the energy.
        Args:
            ene(float): Energy [keV]
        Returns:
            (float): Bragg angle value [deg]
        """
        if self.xtal_sel is None:
            return np.nan
        xtal = self.xtal[self.xtal_sel]
        bragg = xtal.bragg_angle(ene * ur.keV)
        if np.isnan(bragg).any():
            return np.nan

        # convert radians to degrees
        bragg = bragg.to(ur.deg).magnitude
        return bragg

    def bragg2energy(self, bragg):
        """Calculate the energy as function of the bragg angle
        Args:
            bragg(float): Bragg angle [deg]
        Returns:
            (float): Energy [keV]
        """
        if self.xtal_sel is None:
            return np.nan
        xtal = self.xtal[self.xtal_sel]
        energy = xtal.bragg_energy(bragg * ur.deg)
        if np.isnan(energy.magnitude).any():
            return np.nan
        energy = energy.to(ur.keV).magnitude
        return energy

    def get_metadata(self, theta) -> dict:
        if self.xtal_sel is None:
            return dict()
        xtal = self.xtal[self.xtal_sel]

        energy = xtal.bragg_energy(theta)
        if np.isnan(energy.magnitude).any():
            energy = np.nan
        else:
            energy = energy.to(ur.keV).magnitude

        wavelength = xtal.bragg_wavelength(theta)
        if np.isnan(wavelength.magnitude).any():
            wavelength = np.nan
        else:
            wavelength = wavelength.to(ur.m).magnitude

        mdata = {
            "energy": energy,
            "wavelength": wavelength,
            "crystal": {"d_spacing": xtal.d},
        }

        if isinstance(xtal, CrystalPlane):
            mdata["crystal"]["type"] = xtal.crystal.name
            mdata["crystal"]["reflection"] = tuple(xtal.plane)
        elif isinstance(xtal, Multilayer):
            mdata["crystal"]["type"] = f"multilayer: {xtal.name}"
        else:
            mdata["crystal"]["type"] = "unknown"

        return mdata


class Multilayer:
    def __init__(self, config):
        self.__config = config
        self.__name = config["name"]
        self.thickness1 = self.config.get("thickness1", None)
        self.thickness2 = self.config.get("thickness2", None)
        self.ml_file = self.config.get("delta_bar", None)
        self.lut_file = None
        if self.thickness1 is not None and self.thickness2 is not None:
            self.d = ((self.thickness1 + self.thickness2) * 1e-9) * ur.m
            if self.ml_file is not None:
                self.create_lut_from_ml_file()
        else:
            dspacing = self.config.get("dspacing", None)
            if dspacing is not None:
                self.d = (dspacing * 1e-9) * ur.m
            else:
                self.d = None
                self.lut_file = self.config.get("lookup_table", None)
                if self.lut_file is not None:
                    self.create_lut_from_lut_file()
                else:
                    raise RuntimeError(
                        f"Multilayer {self.name}: Wrong yml configuration"
                    )

    @property
    def name(self):
        return self.__name

    @property
    def config(self):
        return self.__config

    def bragg_min_max(self, unit="deg"):
        """Get the theoretical min and max bragg angle values.
        Args:
            unit(str): The unit of the value as string ("deg", "mrad", "rad").
                       Default value: "deg"
        Returns:
            (tupple): The min and max theoretical value [unit]
        """
        if self.ml_file or self.lut_file:
            min_th = (self.en2bragg.min_y() * ur.rad).to(unit).magnitude
            max_th = (self.en2bragg.max_y() * ur.rad).to(unit).magnitude
            return min_th, max_th
        return ()

    def __info__(self):
        info_str = ""
        if self.thickness1 is not None and self.thickness2 is not None:
            info_str += f"Thickness Material #1: {self.thickness1*ur.nm}\n"
            info_str += f"Thickness Material #2: {self.thickness2*ur.nm}\n"
            dspacing = self.d.to("nm")
            info_str += f"d-spacing: {dspacing}\n"
            if self.ml_file is not None:
                min_en = (self.en2bragg.min_x() * ur.J).to("keV").magnitude
                max_en = (self.en2bragg.max_x() * ur.J).to("keV").magnitude
                min_th = np.degrees(self.en2bragg.min_y())
                max_th = np.degrees(self.en2bragg.max_y())

                info_str += f"delta_bar file: {self.ml_file}\n"
                info_str += f"Energy [keV]: {min_en:.3f} - {max_en:.3f}\n"
                info_str += f"Bragg [deg] : {max_th:.3f} - {min_th:.3f}\n"
        else:
            if self.d is not None:
                dspacing = self.d.to("nm")
                info_str += f"d-spacing: {dspacing}\n"
            else:
                if self.lut_file is not None:
                    min_en = (self.en2bragg.min_x() * ur.J).to("keV").magnitude
                    max_en = (self.en2bragg.max_x() * ur.J).to("keV").magnitude
                    min_th = np.degrees(self.en2bragg.min_y())
                    max_th = np.degrees(self.en2bragg.max_y())

                    info_str += f"Lookup table file: {self.lut_file}\n"
                    info_str += f"Energy [keV]: {min_en:.3f} - {max_en:.3f}\n"
                    info_str += f"Bragg [deg]: {max_th:.4f} - {min_th:.4f}\n"

                else:
                    raise RuntimeError("THIS ERROR SHOULD NEVER HAPPENED !!!\n")

        return info_str

    def create_lut_from_ml_file(self):
        """Create a lookup table from multilayer file. The file format is the
        standard, defined by the multilayer lab.
        """
        if self.ml_file is not None:
            arr = np.loadtxt(self.ml_file, comments="#").transpose()
            arr_energy = np.copy((arr[0] * ur.keV).to(ur.J))
            arr_theta = np.arcsin(
                np.sqrt(arr[5] + np.power(hc / (2.0 * self.d * arr_energy), 2))
            )

            self.en2bragg = xcalibu.Xcalibu()
            self.en2bragg.set_calib_name(f"{self.name}_bragg")
            self.en2bragg.set_calib_time(0)
            self.en2bragg.set_calib_type("TABLE")
            self.en2bragg.set_reconstruction_method("INTERPOLATION")
            self.en2bragg.set_raw_x(arr_energy.magnitude)
            self.en2bragg.set_raw_y(arr_theta.magnitude)

            arr_flip_theta = np.flip(arr_theta)
            arr_flip_energy = np.flip(arr_energy)
            self.bragg2en = xcalibu.Xcalibu()
            self.bragg2en.set_calib_name(f"{self.name}_bragg")
            self.bragg2en.set_calib_time(0)
            self.bragg2en.set_calib_type("TABLE")
            self.bragg2en.set_reconstruction_method("INTERPOLATION")
            self.bragg2en.set_raw_x(arr_flip_theta.magnitude)
            self.bragg2en.set_raw_y(arr_flip_energy.magnitude)

    def create_lut_from_lut_file(self):
        """Create a Lookup table from a file. The file should be in format of
        two columns: Energy [eV] bragg_angle [rad]
        """
        if self.lut_file is not None:
            arr = np.loadtxt(self.lut_file, comments="#").transpose()
            arr_energy = np.copy(((arr[0] / 1000.0) * ur.keV).to(ur.J))
            arr_theta = np.copy(arr[1] * ur.radians)

            self.en2bragg = xcalibu.Xcalibu()
            self.en2bragg.set_calib_name(f"{self.name}_bragg")
            self.en2bragg.set_calib_time(0)
            self.en2bragg.set_calib_type("TABLE")
            self.en2bragg.set_reconstruction_method("INTERPOLATION")
            self.en2bragg.set_raw_x(arr_energy.magnitude)
            self.en2bragg.set_raw_y(arr_theta.magnitude)

            arr_flip_theta = np.flip(np.copy(arr_theta))
            arr_flip_energy = np.flip(np.copy(arr_energy))
            self.bragg2en = xcalibu.Xcalibu()
            self.bragg2en.set_calib_name(f"{self.name}_bragg")
            self.bragg2en.set_calib_time(0)
            self.bragg2en.set_calib_type("TABLE")
            self.bragg2en.set_reconstruction_method("INTERPOLATION")
            self.bragg2en.set_raw_x(arr_flip_theta.magnitude)
            self.bragg2en.set_raw_y(arr_flip_energy.magnitude)

    @units(wavelength="m", result="J")
    def wavelength_to_energy(self, wavelength):
        """
        Returns photon energy [J] for the given wavelength [m]

        Args:
            wavelength (float): photon wavelength [m]
        Returns:
            float: photon energy [J]
        Raises:
            ZeroDivisionError: If the bragg angle = 0.
        """
        if wavelength:
            return hc / wavelength
        raise ZeroDivisionError("Cannot calculate energy for bragg angle = 0")

    @units(energy="J", result="m")
    def energy_to_wavelength(self, energy):
        """
        Returns photon wavelength (m) for the given energy (J)

        Args:
            energy (float): photon energy (J)
        Returns:
            float: photon wavelength (m)
        """
        if energy:
            return hc / energy
        raise ZeroDivisionError("Cannot calculate energy for bragg angle = 0")

    @units(theta="rad", result="m")
    def bragg_wavelength(self, theta, n=1):
        """
        Return a bragg wavelength (m) for the given theta and distance between
        lattice planes.

        Args:
            theta (float): scattering angle (rad)
            n (int): order of reflection. Non zero positive integer (default: 1)
        Returns:
            float: bragg wavelength (m) for the given theta and lattice distance
        """
        return 2.0 * self.d * math.sin(theta)

    @units(theta="rad", result="J")
    def bragg_energy(self, theta, n=1):
        """
        Return a bragg energy for the given theta and distance between lattice
        planes.

        Args:
            theta (float): scattering angle (rad)
            n (int): order of reflection. Non zero positive integer (default: 1)
        Returns:
            float: bragg energy (J) for the given theta and lattice distance
        """
        if self.ml_file is None and self.lut_file is None:
            return self.wavelength_to_energy(self.bragg_wavelength(theta, n=n))
        if self.bragg2en.min_x() <= theta.magnitude <= self.bragg2en.max_x():
            return self.bragg2en.get_y(theta.magnitude) * ur.J
        return (np.nan) * ur.J

    @units(energy="J", result="rad")
    def bragg_angle(self, energy):
        """
        Return a bragg angle [rad] for the given theta and distance between
        lattice planes.

        Args:
            energy (float): energy [J]
            d (float): interplanar distance between lattice planes [m]
            n (int): order of reflection. Non zero positive integer (default: 1)
        Returns:
            (float): bragg angle [rad] for the given theta and lattice distance
        """
        if self.ml_file is None and self.lut_file is None:
            return np.arcsin(hc / (2.0 * self.d * energy))
        if self.en2bragg.min_x() <= energy.magnitude <= self.en2bragg.max_x():
            return self.en2bragg.get_y(energy.magnitude) * ur.rad
        return (np.nan) * ur.rad


class TrackTableMulti:
    def __init__(self, tracked_axes):
        self.__tracked_axes = tracked_axes

    def plot(self, axis):
        """display table points for given axis on a plot"""
        if isinstance(axis, str):
            axis_name = axis
        else:
            axis_name = axis.name
        for axs in self.__tracked_axes():
            if axs.name == axis_name:
                return axs.track_table.plot()
        return None

    def __info__(self):
        """print the calib tables in use for all tracked axes"""
        axes = [axis for axis in self.__tracked_axes() if axis.track_mode == "table"]
        if len(axes) == 0:
            return "No axis currently tracked with table mode"
        title = ["Energy"] + [axis.name for axis in axes]

        energies = [axis.track_table.calib.x_raw for axis in axes]
        energies = np.unique(np.concatenate(energies))

        def position(axis, energy):
            try:
                return axis.track_table.calib.get_y(energy)
            except Exception:
                return None

        data = []
        for energy in energies:
            data.append([energy] + [position(axis, energy) for axis in axes])

        mystr = tabulate.tabulate(data, headers=title)

        return "\n" + mystr

    def setpoint(self):
        """add current position (energy, motor) to table for all tracked axes"""
        for axis in self.__tracked_axes():
            axis.track_table.setpoint()

    def delpoint(self, energy=None):
        """delete current energy from table for all tracked axes"""
        for axis in self.__tracked_axes():
            axis.track_table.delpoint(energy)

    def save(self):
        """save table calib files to beamline configuration for all tracked axes"""
        for axis in self.__tracked_axes():
            axis.track_table.save()

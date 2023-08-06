# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Calculation motors definitions"""

import math
import numpy as np

from bliss.physics.units import ur
from bliss.controllers.motor import CalcController


class MonochromatorCalcMotorBase(CalcController):
    """Base class"""

    def __init__(self, *args, **kwargs):
        CalcController.__init__(self, *args, **kwargs)

        self.mono = None

        if "approximation" in self.config.config_dict:
            self.approx = float(self.config.get("approximation"))
        else:
            self.approx = 0.0

    def __info__(self):
        info_str = f"CONTROLLER: {self.__class__.__name__}\n"

        return info_str

    def get_axis_info(self, axis):
        """Get the info for axis"""
        info_str = ""
        return info_str

    def set_mono(self, mono):
        """Define mono property"""
        self.mono = mono

    def pseudos_are_moving(self):
        """Check if pseudo axis are moving"""
        for axis in self.pseudos:
            if axis.is_moving:
                return True
        return False


class EnergyCalcMotor(MonochromatorCalcMotorBase):
    """Energy Calculation Motor"""

    def calc_from_real(self, real_positions):
        """Calculate the energy from the position of the real motor.
        Args:
            real_positions(dict): Dictionary of the real motor positions.
        Returns:
            (dict): Dictionary with the energy position(s) [KeV]
        """

        pseudos_dict = {}

        if self.mono is not None and self.mono.xtal_sel is not None:
            unit = self.reals[0].unit or "deg"
            value = (
                (real_positions["bragg"] * ur.parse_units(self.reals[0].unit))
                .to("deg")
                .magnitude
            )
            ene = self.mono.bragg2energy(value)
            if not np.isnan(ene).any():
                unit = self.pseudos[0].unit or "keV"
                ene = (ene * ur.keV).to(unit).magnitude
            pseudos_dict["energy"] = ene
        else:
            pseudos_dict["energy"] = np.nan

        return pseudos_dict

    def calc_to_real(self, positions_dict):
        """Calculate the position of the real motor from the energy.
        Args:
            positions_dict (dict): Dictionary with the energy position(s)
        Returns:
            (dict): Dictionary of the real motor positions.
        """
        reals_dict = {}
        if (
            self.mono is not None
            and self.mono.xtal_sel is not None
            and not np.isnan(positions_dict["energy"]).any()
        ):
            unit = self.pseudos[0].unit or "keV"
            ene = (positions_dict["energy"] * ur.parse_units(unit)).to("keV").magnitude
            bragg = self.mono.energy2bragg(ene)
            unit = self.reals[0].unit or "deg"
            reals_dict["bragg"] = (bragg * ur.deg).to(unit).magnitude
        else:
            for axis in self.reals:
                reals_dict[self._axis_tag(axis)] = axis.position

        return reals_dict


class BraggFixExitCalcMotor(MonochromatorCalcMotorBase):
    """
    Bragg Fix Exit Calculation Motor
    """

    def calc_from_real(self, real_positions):

        pseudos_dict = {}

        bragg = 0.0
        rbragg = 0.0
        if self.mono is not None:
            bragg = self.mono.xtal2bragg(real_positions["xtal"])
            rbragg = real_positions["bragg"]

            if (
                math.isclose(bragg, rbragg, abs_tol=self.approx)
            ) or self.pseudos_are_moving():
                pseudos_dict["bragg_fix_exit"] = real_positions["bragg"]
            else:
                pseudos_dict["bragg_fix_exit"] = np.nan
        else:
            pseudos_dict["bragg_fix_exit"] = np.nan

        return pseudos_dict

    def calc_to_real(self, positions_dict):
        """Calculate the position of the real motor from the Fix Exit Bragg
        Args:
            positions_dict (dict): Dictionary with the Fix Exit Bragg angle.
        Returns:
            (dict): Dictionary of the real motor positions.
        """

        reals_dict = {}

        if (
            self.mono is not None
            and not np.isnan(positions_dict["bragg_fix_exit"]).any()
        ):
            reals_dict["bragg"] = positions_dict["bragg_fix_exit"]
            reals_dict["xtal"] = self.mono.bragg2xtal(positions_dict["bragg_fix_exit"])
        else:
            for axis in self.reals:
                reals_dict[self._axis_tag(axis)] = axis.position

        return reals_dict


class EnergyTrackingCalcMotor(MonochromatorCalcMotorBase):
    """
    Energy + tracker Calculated motor
    """

    def __init__(self, *args, **kwargs):
        MonochromatorCalcMotorBase.__init__(self, *args, **kwargs)

    def energy2tracker(self, axis, energy):
        return axis.tracker.energy2tracker(axis, energy)

    def tracker2energy(self, axis, gap):
        return axis.tracker.tracker2energy(axis, gap)

    def calc_from_real(self, reals_dict):

        pseudos_dict = {}

        energy = reals_dict["energy"]

        in_pos = True
        for axis in self.reals:
            tag = self._axis_tag(axis)
            if tag != "energy":
                if axis.track:
                    track = axis.tracker.energy2tracker(axis, energy)
                    rtrack = reals_dict[tag]
                    if not math.isclose(track, rtrack, abs_tol=self.approx):
                        in_pos = False

        if in_pos or self.pseudos_are_moving():
            pseudos_dict["energy_track"] = energy
        else:
            pseudos_dict["energy_track"] = np.nan

        return pseudos_dict

    def calc_to_real(self, pseudos_dict):

        reals_dict = {}

        energy = pseudos_dict["energy_track"]

        if not np.isnan(energy).any():
            ##In [24]: np.array([not np.isnan(x) for x in np.array(list([1,2, 3]))]).all()
            ##Out[24]: True
            #
            ##In [25]: np.array([not np.isnan(x) for x in np.array(list([1,2, np.nan]))]).all()
            ##Out[25]: False
            #
            # if isinstance(energy, np.ndarray):
            #    # Ensure that all elements of energy array are *not NaN*.
            #    ok = np.array([not np.isnan(x) for x in np.array(energy)]).all()
            # else:
            #    # Ensure that energy is  *not NaN*.
            #    ok = not np.isnan(energy)
            #
            # if ok:
            reals_dict["energy"] = energy
            for axis in self.reals:
                tag = self._axis_tag(axis)
                if tag != "energy":
                    if axis.track:
                        reals_dict[tag] = axis.tracker.energy2tracker(axis, energy)
                    else:
                        reals_dict[tag] = axis.position
        else:
            for axis in self.reals:
                reals_dict[self._axis_tag(axis)] = axis.position

        return reals_dict

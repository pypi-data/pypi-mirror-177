# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2020 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from .diff_base import Diffractometer


class DiffK6C(Diffractometer):

    PSEUDOS_FMT = """\
H K L = {pos[hkl_h]:f} {pos[hkl_k]:f} {pos[hkl_l]:f}
TWO THETA = {pos[tth2_tth]:f}
Alpha = {pos[incidence_incidence]:.5g}  Beta = {pos[emergence_emergence]:.5g}
"""

    # def show(self):
    ### TODO ### making a nice, "pa" spec-like output

    @property
    def eulerian_par(self):
        vals = self._geometry.get_mode_pars("eulerians", "eulerians")
        return vals["solutions"]

    @eulerian_par.setter
    def eulerian_par(self, solutions):
        if solutions in (0, 1):
            self._geometry.set_mode_pars(
                "eulerians", "eulerians", {"solutions": solutions}
            )
        else:
            raise ValueError(
                "solutions must be 0 or 1 to select the first or second solution"
            )
        self._calc_geo()

    @property
    def hklpars(self):
        current_mode = self.hklmode
        pars_dict = self.geometry.get_mode_pars("hkl", current_mode)
        print(f"HKL mode {current_mode}\n")
        for key in pars_dict.keys():
            print(f"{key:10s} : {pars_dict[key]}")

    def set_hklpars(self):
        current_mode = self.hklmode
        pars_dict = self.geometry.get_mode_pars("hkl", current_mode)
        for key in pars_dict.keys():
            oldval = pars_dict[key]
            newval = input(f" {key} ({oldval}) ? ")
            if newval:
                pars_dict[key] = float(newval)
        self.geometry.set_mode_pars("hkl", current_mode, pars_dict)

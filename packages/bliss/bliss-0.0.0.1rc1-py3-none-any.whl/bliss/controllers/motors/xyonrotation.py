# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.
"""
Virtual X and Y axis which stay on top of a rotation
"""

import numpy
from bliss.controllers.motor import CalcController
from bliss.common.utils import object_method


class XYOnRotation(CalcController):
    """
    Virtual X and Y axis on top of a rotation

    .. code-block:: yaml

        class: XYOnRotation

        # if rotation is inverted
        # optional, default is False
        inverted: False

        # if rotation angle is in radian
        # optional, default is False == degree
        # deprecated, prefer setting unit "deg"/"rad" to the rotation axis
        radian: False           # optional

        # Use dial instead of user position for the rotation
        # optional, default is False
        use_dial_rot: True

        axes:
            - name: $rot
              tags: real rot
            - name: $px
              tags: real rx     # real X
            - name: $py
              tags: real ry     # real Y
            - name: sampx
              tags: x
            - name: sampy
              tags: y
    """

    def __init__(self, *args, **kwargs):
        CalcController.__init__(self, *args, **kwargs)
        self.__inverted = 1
        self.__radian = None
        self.__use_dial_rot = False

    def _init(self):
        CalcController._init(self)
        try:
            self._finalize_init()
        except:
            # Clean up stuffs in case of problems
            self.close()
            raise

    def _finalize_init(self):
        """Finalize the initialization when everything was loaded"""

        rot = self._tagged["rot"][0]
        if rot.unit == "rad":
            # Sanity check if randian property was defined
            if self.__radian is False:
                raise ValueError("Radian property defined while rotation unit mismatch")
            self.__radian = True
        elif rot.unit == "deg":
            # Sanity check if randian property was defined
            if self.__radian is True:
                raise ValueError("Radian property defined while rotation unit mismatch")
            self.__radian = False
        else:
            if self.__radian is None:
                # Default value
                self.__radian = False

        rx = self._tagged["rx"][0]
        ry = self._tagged["ry"][0]
        assert (
            rx.unit == ry.unit
        ), f"Real motors must use the same units (found '{rx.name}' with '{rx.unit}' and '{ry.name}' with '{ry.unit}')"
        unit = rx.unit
        if unit is not None:
            cx = self._tagged["x"][0]
            cy = self._tagged["y"][0]
            if cx.unit is None:
                cx._unit = unit
            if cy.unit is None:
                cy._unit = unit
            assert (
                cx.unit == unit
            ), f"Calc motors must the real motor unit (found '{cx.name}' with '{cx.unit}' and '{rx.name}' with '{rx.unit}')"
            assert (
                cy.unit == unit
            ), f"Calc motors must the real motor unit (found '{cy.name}' with '{cy.unit}' and '{rx.name}' with '{rx.unit}')"

    def initialize(self):
        # add rotation offset in motor settings
        self.axis_settings.add("rotation_offset", float)
        CalcController.initialize(self)
        try:
            inverted = self.config.get("inverted", bool)
        except KeyError:
            self.__inverted = 1
        else:
            self.__inverted = -1 if inverted else 1

        try:
            use_dial_rot = self.config.get("use_dial_rot", bool)
        except KeyError:
            self.__use_dial_rot = False
        else:
            self.__use_dial_rot = use_dial_rot

        self.__radian = self.config.get("radian", bool)

    def initialize_axis(self, axis):
        CalcController.initialize_axis(self, axis)

    def calc_from_real(self, real_positions):
        rx = real_positions["rx"]
        ry = real_positions["ry"]
        if self.__use_dial_rot:
            rot_axis = self._tagged["rot"][0]
            userrot = real_positions["rot"]
            rot = rot_axis.user2dial(userrot)
        else:
            rot = real_positions["rot"]
        rot += self._tagged["x"][0].rotation_offset()
        if self.__radian:
            rot_rad = rot
        else:
            rot_rad = rot / 180 * numpy.pi
        rot_rad *= self.__inverted

        return {
            "x": rx * numpy.cos(rot_rad) - ry * numpy.sin(rot_rad),
            "y": rx * numpy.sin(rot_rad) + ry * numpy.cos(rot_rad),
        }

    def calc_to_real(self, positions_dict):
        x = positions_dict["x"]
        y = positions_dict["y"]
        rot_axis = self._tagged["rot"][0]
        if self.__use_dial_rot:
            rot = rot_axis.dial
        else:
            rot = rot_axis.position
        rot += self._tagged["x"][0].rotation_offset()
        if self.__radian:
            rot_rad = rot
        else:
            rot_rad = rot / 180 * numpy.pi
        rot_rad *= self.__inverted

        return {
            "rx": x * numpy.cos(rot_rad) + y * numpy.sin(rot_rad),
            "ry": -x * numpy.sin(rot_rad) + y * numpy.cos(rot_rad),
        }

    @object_method(types_info=("None", "float"))
    def rotation_offset(self, axis, offset=None):
        """
        get/set rotation offset between rotation motor and
        virtual axes
        """
        if offset is None:
            rotation_offset = axis.settings.get("rotation_offset")
            return rotation_offset if rotation_offset else 0
        else:
            for axis in self.axes.values():
                axis.settings.set("rotation_offset", offset)

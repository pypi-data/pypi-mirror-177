# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.
"""
Scan meta is a way to add metadata for any scans.

Categories will be represent by groups underneath the scan
group except from POSITIONERS.
"""
__all__ = ["get_user_scan_meta"]

import time
import gevent

import copy as copy_module
import enum
import pprint

from bliss import global_map
from bliss.common.protocols import HasMetadataForScan, HasMetadataForScanExclusive
from bliss.common.logtools import user_error, user_warning
from bliss.common.utils import deep_update


class META_TIMING(enum.Flag):
    START = enum.auto()
    END = enum.auto()
    PREPARED = enum.auto()


USER_SCAN_META = None


class ScanMetaCategory:
    """Provides an API part of the metadata belonging to one category"""

    def __init__(self, category, metadata, timing):
        """
        :param CATEGORIES category:
        :param dict metadata: CATEGORIES -> str or callable
        :param dict timing: CATEGORIES -> META_TIMING
        """
        self._category = category
        self._metadata = metadata
        self._timing = timing

    @property
    def category(self):
        return self._category

    @property
    def name(self):
        return self._category.name

    @property
    def metadata(self):
        return self._metadata.setdefault(self.category, dict())

    @property
    def timing(self):
        return self._timing.setdefault(self.category, META_TIMING.START)

    @timing.setter
    def timing(self, timing):
        self._timing[self.category] = timing

    def _parse_metadata_name(self, name_or_device):
        """
        :param name_or_device: string or an object with a name property
        :returns str or None:
        """
        if isinstance(name_or_device, str):
            if not name_or_device:
                user_error("a name is required to publish scan metadata")
                return None
            return name_or_device
        else:
            try:
                name = name_or_device.name
                if name:
                    return name
            except AttributeError:
                pass
            user_error("%r needs a name to publish scan metadata", name_or_device)
            return None

    def set(self, name_or_device, values):
        """
        :param name_or_device: string or an object with a name property
        :param callable or dict values: callable needs to return a dictionary
        """
        name = self._parse_metadata_name(name_or_device)
        if name:
            self.metadata[name] = values

    def is_set(self, name_or_device) -> bool:
        """
        :param name_or_device: string or an object with a name property
        :returns bool:
        """
        name = self._parse_metadata_name(name_or_device)
        return name in self.metadata

    def remove(self, name_or_device):
        """
        :param name_or_device: string or an object with a name property
        """
        name = self._parse_metadata_name(name_or_device)
        metadata = self.metadata
        metadata.pop(name, None)
        if not metadata:
            self._metadata.pop(self.category, None)

    @property
    def names(self):
        return list(self.metadata.keys())

    def __info__(self):
        s = pprint.pformat(self.metadata, indent=2)
        return f"{self.__class__.__name__}{self.name}: \n " + s


class ScanMeta:
    """Register metadata for all scans. The `Scan` object will call `ScanMeta.to_dict`
    to generate the metadata.

    To add static metadata for a particular scan you pass it to the scan as an argument:

        scan_info={"instrument": "mydetector":{"@NX_class": "NXdetector", "myparam": 1}}
        s = loopscan(..., scan_info={"instrument": "mydetector":{"myparam": 1}})
    """

    CATEGORIES = enum.Enum("categories", "INSTRUMENT POSITIONERS TECHNIQUE")

    def __init__(self, metadata=None, timing=None):
        if metadata is None:
            self._metadata = dict()
        else:
            self._metadata = metadata
        if timing is None:
            self._timing = dict()
        else:
            self._timing = timing

    @classmethod
    def categories_names(cls):
        return [cat.name.lower() for cat in cls.CATEGORIES]

    @classmethod
    def add_categories(cls, names):
        names = {s.upper() for s in names}
        original = {m.name for m in cls.CATEGORIES}
        new = original | names
        if original != new:
            cls.CATEGORIES = enum.Enum("categories", " ".join(new))

    @classmethod
    def remove_categories(cls, names):
        names = {s.upper() for s in names}
        original = {m.name for m in cls.CATEGORIES}
        new = original - names
        if original != new:
            cls.CATEGORIES = enum.Enum("categories", " ".join(new))

    def __getattr__(self, name):
        cat = self._scan_meta_category(name)
        if cat is None:
            raise AttributeError(name)
        else:
            return cat

    def _scan_meta_category(self, category_or_name):
        """
        :param CATEGORIES or str category:
        :returns ScanMetaCategory:
        """
        if isinstance(category_or_name, str):
            category_name = category_or_name.upper()
            category = self.CATEGORIES.__members__.get(category_name)
            if not category:
                return
        else:
            # ensure that if category is given, it corresponds to an existing category
            category = category_or_name
            if not any(cat.name == category.name for cat in self.CATEGORIES):
                return
        return ScanMetaCategory(category, self._metadata, self._timing)

    def _profile_metadata_gathering(self, scan=None, timing=META_TIMING.START):
        """Generate metadata for profiling (mimics self.to_dict but not parallelized).
        Return a tuple (name, catname, dt).
        """
        result = []
        for category in list(self._metadata):
            smcategory = self._scan_meta_category(category)
            if smcategory is None:
                # Category was removed
                self._metadata.pop(category, None)
                continue
            if timing not in smcategory.timing:
                # Category metadata should not be generated at this time
                continue
            catname = category.name.lower()
            for name, values in smcategory.metadata.items():
                t0 = time.perf_counter()
                if callable(values):
                    try:
                        values = values(scan)
                    except Exception:
                        err_msg = f"cannot generate metadata from controller {repr(name)} for metadata category {repr(catname)}"
                        user_error(err_msg, exc_info=True)
                        continue
                    if values is None:
                        continue
                dt = time.perf_counter() - t0
                result.append((name, catname, dt))
        return result

    def to_dict(self, scan, timing=META_TIMING.START):
        """Generate metadata (parallelized)"""
        result = {}
        tasks = []
        t0 = time.perf_counter()
        for category in list(self._metadata):
            smcategory = self._scan_meta_category(category)
            if smcategory is None:
                # Category was removed
                self._metadata.pop(category, None)
                continue
            if timing not in smcategory.timing:
                # Category metadata should not be generated at this time
                continue
            catname = category.name.lower()
            for (
                name,
                values,
            ) in smcategory.metadata.items():  # values is a dict or a function or None
                if values is None:
                    continue

                cat_dict = result.setdefault(catname, {})

                if callable(values):
                    # spawn callables
                    tasks.append((catname, gevent.spawn(values, scan)))
                else:
                    deep_update(cat_dict, values)

        # gather callables results
        for catname, task in tasks:
            try:
                values = task.get()
            except Exception:
                err_msg = f"cannot generate metadata from controller {repr(name)} for metadata category {repr(catname)}"
                user_error(err_msg, exc_info=True)
                continue
            if values is None:
                continue
            deep_update(result[catname], values)

        dt = time.perf_counter() - t0
        if dt > 0.15:
            user_warning(
                f"metadata gathering took {dt*1000:.3f}ms, type 'metadata_profiling()' for more details"
            )
        return result

    def clear(self):
        """Clear all metadata"""
        self._metadata.clear()

    def _metadata_copy(self):
        mdcopy = dict()
        for category, metadata in list(self._metadata.items()):
            mdcat = mdcopy[category] = dict()
            for name, values in metadata.items():
                # A deep copy of an object method appears to copy
                # the object itself
                if not callable(values):
                    values = copy_module.deepcopy(values)
                mdcat[name] = values
        return mdcopy

    def copy(self):
        return self.__class__(
            metadata=self._metadata_copy(), timing=copy_module.copy(self._timing)
        )

    def used_categories_names(self):
        return [n.name.lower() for n in self._metadata.keys()]

    def __info__(self):
        s = pprint.pformat(self._metadata, indent=2)
        return f"{self.__class__.__name__}: \n " + s


def fill_positioners(scan):
    suffix = "_start"
    # scan can be None if called from metadata_profiling (see standard.py)
    if scan is not None and scan.state == 3:
        suffix = "_end"
    positioners = dict()
    positioners_dial = dict()
    units = dict()
    for (
        axis,
        disabled,
        error,
        axis_pos,
        axis_dial_pos,
        unit,
    ) in global_map.get_axes_positions_iter(on_error="ERR"):
        if error:
            positioners[axis.name] = error
            positioners_dial[axis.name] = error
            units[axis.name] = unit
        elif not disabled:
            positioners[axis.name] = axis_pos
            positioners_dial[axis.name] = axis_dial_pos
            units[axis.name] = unit

    rd = {
        "positioners" + suffix: positioners,
        "positioners_dial" + suffix: positioners_dial,
    }

    if scan is not None and scan.state != 3:
        rd["positioners_units"] = units

    return rd


def get_user_scan_meta():
    """A single instance is used for the lifetime of the process."""
    global USER_SCAN_META
    if USER_SCAN_META is None:
        USER_SCAN_META = ScanMeta()
        USER_SCAN_META.instrument.set("@NX_class", {"@NX_class": "NXinstrument"})
        USER_SCAN_META.instrument.timing = META_TIMING.END
        USER_SCAN_META.technique.set("@NX_class", {"@NX_class": "NXcollection"})
    return USER_SCAN_META


def get_controllers_scan_meta():
    """A new instance is created for every scan."""
    scan_meta = ScanMeta()
    scan_meta.instrument.set("@NX_class", {"@NX_class": "NXinstrument"})
    scan_meta.positioners.set("positioners", fill_positioners)
    scan_meta.positioners.timing = META_TIMING.START | META_TIMING.END

    for obj in global_map.instance_iter("controllers"):
        if isinstance(obj, HasMetadataForScan):
            if isinstance(obj, HasMetadataForScanExclusive):
                # metadata for this controller has to be gathered by acq. chain
                continue
            if not obj.scan_metadata_enabled:
                continue
            scan_meta.instrument.set(obj, obj._generate_metadata)
    return scan_meta

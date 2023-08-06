# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

# Single source of truth for the version number and the like

copyright = "2015-2022 Beamline Control Unit, ESRF"

try:
    from importlib.metadata import metadata as _metadata
except ModuleNotFoundError:  # for Python <3.8
    from importlib_metadata import metadata as _metadata

_pkg_metadata = dict(_metadata("bliss").items())
author = _pkg_metadata["Author"]
author_email = _pkg_metadata.get("Maintainer-email")
license = _pkg_metadata["License"]
description = _pkg_metadata["Summary"]
url = _pkg_metadata["Home-page"]
version = _pkg_metadata["Version"]

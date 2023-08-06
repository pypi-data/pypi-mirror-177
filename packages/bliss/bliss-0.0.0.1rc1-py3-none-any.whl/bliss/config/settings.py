from bliss.common import deprecation
from blissdata.settings import scan, HashObjSetting  # noqa: F401
from bliss.config.wardrobe import ParametersWardrobe  # noqa: F401

deprecation.deprecated_warning(
    "Module",
    "bliss.config.settings",
    replacement="[blissdata.settings, bliss.config.wardrobe]",
    since_version="1.11",
    skip_backtrace_count=100,
)

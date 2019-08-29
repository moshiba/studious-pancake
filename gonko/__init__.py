import sys
if hasattr(sys, "_called_from_test"):
    __all__ = ["file", "utils"]
    from . import file
    from . import utils
else:
    __all__ = ["file", "parallel", "utils"]
    from . import file
    from . import parallel
    from . import utils

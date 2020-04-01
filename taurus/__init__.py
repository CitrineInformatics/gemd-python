"""Data concepts library."""

import warnings
warnings.warn("The taurus module is deprecated in favor of gemd; "
              "Most functionality can be recovered by replacing 'taurus' with 'gemd' in imports.",
              DeprecationWarning, stacklevel=2)

from gemd import *


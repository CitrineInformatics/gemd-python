"""Base class for categorical values."""
from taurus.entity.value.base_value import BaseValue


class CategoricalValue(BaseValue):
    """
    Base class for categorical values, which are distributions over valid category names.

    All category names must be in unicode.
    """

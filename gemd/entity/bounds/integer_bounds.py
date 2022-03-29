"""Bounds an integer to be between two values."""
from gemd.entity.bounds.base_bounds import BaseBounds, convert_bounds
import gemd.units as units

from typing import Union

DIMENSIONLESS = "dimensionless"


class IntegerBounds(BaseBounds):
    """
    Bounded subset of the integers, parameterized by a lower and upper bound.

    Parameters
    ----------
    lower_bound: int
        Lower endpoint.
    upper_bound: int
        Upper endpoint.
    default_units: str
        An optional string describing the units that must be parseable by Pint, if supplied.
        If this argument is not supplied, the 'dimensionless' string will be used.

    """

    typ = "integer_bounds"

    def __init__(self, lower_bound=None, upper_bound=None, default_units=DIMENSIONLESS):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self._default_units = None
        self.default_units = default_units

        if self.lower_bound is None or abs(self.lower_bound) >= float("inf"):
            raise ValueError("Lower bound must be given and finite: {}".format(self.lower_bound))

        if self.upper_bound is None or abs(self.upper_bound) >= float("inf"):
            raise ValueError("Upper bound must be given and finite")

        if self.upper_bound < self.lower_bound:
            raise ValueError("Upper bound must be greater than or equal to lower bound")

    @property
    def default_units(self):
        """Get default units."""
        return self._default_units

    @default_units.setter
    def default_units(self, default_units):
        if default_units is None:
            raise ValueError("Integer bounds must have units. "
                             "Use 'default_units=None' for the default dimensionless quantity.")
        self._default_units = units.parse_units(default_units)

    def contains(self, bounds: Union[BaseBounds, "BaseValue"]) -> bool:
        """
        Check if another bounds or value object is a subset of this range.

        The other object must also be an Integer and its lower and upper bound must *both*
        be within the range of this bounds object.

        Parameters
        ----------
        bounds: Union[BaseBounds, BaseValue]
            Other bounds or value object to check.

        Returns
        -------
        bool
            True if the other object is contained by this bounds.

        """
        from gemd.entity.value.base_value import BaseValue

        if not super().contains(bounds):
            return False
        if isinstance(bounds, BaseValue):
            bounds = bounds._to_bounds()
        if not isinstance(bounds, IntegerBounds):
            return False
        if (bounds.default_units == DIMENSIONLESS) ^ (self.default_units == DIMENSIONLESS):
            raise ValueError("Unit mismatch, cannot compare dimensional and dimensionless bounds")

        lower, upper = convert_bounds(self.lower_bound, self.upper_bound,
                                      self.default_units, bounds.default_units)
        if lower is None:
            return False

        return bounds.lower_bound >= int(lower) and bounds.upper_bound <= int(upper)

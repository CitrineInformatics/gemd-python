"""Bound a real number to be between two values."""
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.value.base_value import BaseValue
from taurus.entity.value.continuous_value import ContinuousValue
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.entity.value.uniform_real import UniformReal
import taurus.units as units


class RealBounds(BaseBounds):
    """Bounded subset of the real numbers, parameterized by a lower and upper bound."""

    typ = "real_bounds"

    def __init__(self, lower_bound=None, upper_bound=None, default_units=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self._default_units = None
        self.default_units = default_units

        if self.lower_bound is None or abs(self.lower_bound) >= float("inf"):
            raise ValueError("Lower bound must be given and finite: {}".format(self.lower_bound))

        if self.upper_bound is None or abs(self.upper_bound) >= float("inf"):
            raise ValueError("Upper bound must be given and finite")

    @property
    def default_units(self):
        """Get default units."""
        return self._default_units

    @default_units.setter
    def default_units(self, default_units):
        if default_units is None:
            raise ValueError("Real bounds must have units. "
                             "Use an empty string for a dimensionless quantity.")
        self._default_units = units.parse_units(default_units)

    def validate(self, value: BaseValue) -> bool:
        """Check if value is within bounds."""
        if not super().validate(value):
            return False
        if not isinstance(value, ContinuousValue):
            return False

        lower, upper = self._convert_bounds(value.units)

        if lower is None:
            return False

        if isinstance(value, NominalReal):
            return upper >= value.nominal >= lower

        # Normal distributions are interpreted as truncated normals,
        # so long as their median value is within the bounds
        if isinstance(value, NormalReal):
            return upper >= value.mean >= lower

        if isinstance(value, UniformReal):
            return upper >= value.upper_bound and lower <= value.lower_bound

    def contains(self, bounds: BaseBounds) -> bool:
        """Check if another bounds is a subset."""
        if not super().contains(bounds):
            return False
        if not isinstance(bounds, RealBounds):
            return False

        lower, upper = self._convert_bounds(bounds.default_units)
        if lower is None:
            return False

        return bounds.lower_bound >= lower and bounds.upper_bound <= upper

    def _convert_bounds(self, target_units):
        """Convert the bounds to the target unit system, or None if not possible."""
        # if neither have units, then just return the bounds
        if not self.default_units and not target_units:
            return self.lower_bound, self.upper_bound
        # if either have units but both don't, then we can't return anything
        elif not self.default_units or not target_units:
            return None, None
        # if both have units, then we can try to convert
        else:
            try:
                lower_bound = units.convert_units(
                    self.lower_bound, self.default_units, target_units)
                upper_bound = units.convert_units(
                    self.upper_bound, self.default_units, target_units)
                return lower_bound, upper_bound
            except units.IncompatibleUnitsError:
                return None, None

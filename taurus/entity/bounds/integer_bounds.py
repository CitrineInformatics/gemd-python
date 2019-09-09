"""Bounds an integer to be between two values."""
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.value.base_value import BaseValue
from taurus.entity.value.integer_value import IntegerValue
from taurus.entity.value.nominal_integer import NominalInteger
from taurus.entity.value.uniform_integer import UniformInteger


class IntegerBounds(BaseBounds):
    """Bounded subset of the integers, parameterized by a lower and upper bound."""

    typ = "integer_bounds"

    def __init__(self, lower_bound=None, upper_bound=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        if self.lower_bound is None or abs(self.lower_bound) >= float("inf"):
            raise ValueError("Lower bound must be given and finite: {}".format(self.lower_bound))

        if self.upper_bound is None or abs(self.upper_bound) >= float("inf"):
            raise ValueError("Upper bound must be given and finite")

    def validate(self, value: BaseValue) -> bool:
        """Checks if a value is an integer within the bounds."""
        if not super().validate(value):
            return False
        if not isinstance(value, IntegerValue):
            return False

        if isinstance(value, NominalInteger):
            return self.upper_bound >= value.nominal >= self.lower_bound

        if isinstance(value, UniformInteger):
            return self.upper_bound >= value.upper_bound and self.lower_bound <= value.lower_bound

    def contains(self, bounds: BaseBounds) -> bool:
        """Check if another bounds is a subset of this range."""
        if not super().contains(bounds):
            return False
        if not isinstance(bounds, IntegerBounds):
            return False

        return bounds.lower_bound >= self.lower_bound and bounds.upper_bound <= self.upper_bound

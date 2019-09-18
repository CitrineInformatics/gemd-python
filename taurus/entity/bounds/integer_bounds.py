"""Bounds an integer to be between two values."""
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.value.base_value import BaseValue
from taurus.entity.value.integer_value import IntegerValue
from taurus.entity.value.nominal_integer import NominalInteger
from taurus.entity.value.uniform_integer import UniformInteger


class IntegerBounds(BaseBounds):
    """
    Bounded subset of the integers, parameterized by a lower and upper bound.

    Parameters
    ----------
    lower_bound: int
        Lower endpoint.
    upper_bound: int
        Upper endpoint.

    """

    typ = "integer_bounds"

    def __init__(self, lower_bound=None, upper_bound=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        if self.lower_bound is None or abs(self.lower_bound) >= float("inf"):
            raise ValueError("Lower bound must be given and finite: {}".format(self.lower_bound))

        if self.upper_bound is None or abs(self.upper_bound) >= float("inf"):
            raise ValueError("Upper bound must be given and finite")

    def validate(self, value: BaseValue) -> bool:
        """
        Checks if a value is an integer within the bounds.

        Parameters
        ----------
        value: BaseValue
            Value to validate. In order to be valid, must be an
            :py:class:`IntegerValue <taurus.entity.value.integer_value.IntegerValue>`
            and be between the lower and upper bound.

        Returns
        -------
        bool
            True if the value is between the lower and upper bound.

        """
        if not super().validate(value):
            return False
        if not isinstance(value, IntegerValue):
            return False

        if isinstance(value, NominalInteger):
            return self.upper_bound >= value.nominal >= self.lower_bound

        if isinstance(value, UniformInteger):
            return self.upper_bound >= value.upper_bound and self.lower_bound <= value.lower_bound

    def contains(self, bounds: BaseBounds) -> bool:
        """
        Check if another bounds is a subset of this range.

        The other bounds must also be an IntegerBounds and its lower and upper bound must *both*
        be within the range of this bounds object.

        Parameters
        ----------
        bounds: BaseBounds
            Other bounds object to check.

        Returns
        -------
        bool
            True if the other bounds is contained by this bounds.

        """
        if not super().contains(bounds):
            return False
        if not isinstance(bounds, IntegerBounds):
            return False

        return bounds.lower_bound >= self.lower_bound and bounds.upper_bound <= self.upper_bound

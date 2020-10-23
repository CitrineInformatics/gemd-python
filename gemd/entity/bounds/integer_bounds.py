"""Bounds an integer to be between two values."""
from gemd.entity.bounds.base_bounds import BaseBounds

from typing import Union


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

        if self.upper_bound < self.lower_bound:
            raise ValueError("Upper bound must be greater than or equal to lower bound")

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

        return bounds.lower_bound >= self.lower_bound and bounds.upper_bound <= self.upper_bound

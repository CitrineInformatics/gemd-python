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

    def union(self, *others: Union["IntegerBounds", "IntegerValue"]) -> "IntegerBounds":
        """
        Return the union of this bounds and other bounds.

        The others list must also be Integer Bounds or Values.

        Parameters
        ----------
        others: Union[IntegerBounds, IntegerValue]
            Other bounds or value objects to include.

        Returns
        -------
        IntegerBounds
            The union of this bounds and the passed bounds

        """
        from gemd.entity.value.integer_value import IntegerValue

        if any(not isinstance(x, (IntegerBounds, IntegerValue)) for x in others):
            misses = {type(x).__name__
                      for x in others
                      if not isinstance(x, (IntegerBounds, IntegerValue))}
            raise TypeError(f"union requires consistent typing; expected integer, found {misses}")
        lower = self.lower_bound
        upper = self.upper_bound
        for bounds in others:
            if isinstance(bounds, IntegerValue):
                bounds = bounds._to_bounds()
            if bounds.lower_bound < lower:
                lower = bounds.lower_bound
            if bounds.upper_bound > upper:
                upper = bounds.upper_bound
        return IntegerBounds(lower_bound=lower, upper_bound=upper)

    def update(self, *others: Union["IntegerBounds", "IntegerValue"]):
        """
        Update this bounds to include other bounds.

        The others list must also be Categorical Bounds or Values.

        Parameters
        ----------
        others: Union[IntegerBounds, IntegerValue]
            Other bounds or value objects to include.

        """
        result = self.union(*others)
        self.lower_bound = result.lower_bound
        self.upper_bound = result.upper_bound

"""Bounds an integer to be between two values."""
from math import isfinite
from typing import TypeVar, Union

from gemd.entity.bounds.base_bounds import BaseBounds

__all__ = ["IntegerBounds"]
IntegerBoundsType = TypeVar("IntegerBoundsType", bound="IntegerBounds")
BaseValueType = TypeVar("BaseValueType", bound="BaseValue")  # noqa: F821
IntegerValueType = TypeVar("IntegerValueType", bound="IntegerValue")  # noqa: F821


class IntegerBounds(BaseBounds, typ="integer_bounds"):
    """
    Bounded subset of the integers, parameterized by a lower and upper bound.

    Parameters
    ----------
    lower_bound: int
        The lower endpoint (inclusive) of the permitted range.
    upper_bound: int
        The upper endpoint (inclusive) of the permitted range.
    """

    def __init__(self, lower_bound: int, upper_bound: int):
        self._lower_bound = None
        self._upper_bound = None

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @property
    def lower_bound(self) -> int:
        """The lower endpoint of the permitted range."""
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value: int):
        """Set the lower endpoint of the permitted range."""
        if value is None or not isfinite(value) or int(value) != float(value):
            raise ValueError(f"Lower bound must be given, integer and finite: {value}")
        if self.upper_bound is not None and value > self.upper_bound:
            raise ValueError(f"Upper bound ({self.upper_bound}) must be "
                             f"greater than or equal to lower bound ({value})")
        self._lower_bound = int(value)

    @property
    def upper_bound(self) -> int:
        """The upper endpoint of the permitted range."""
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, value: int):
        """Set the upper endpoint of the permitted range."""
        if value is None or not isfinite(value) or int(value) != float(value):
            raise ValueError(f"Upper bound must be given, integer and finite: {value}")
        if self.lower_bound is not None and value < self.lower_bound:
            raise ValueError(f"Upper bound ({value}) must be "
                             f"greater than or equal to lower bound ({self.lower_bound})")
        self._upper_bound = int(value)

    def contains(self, bounds: Union[BaseBounds, BaseValueType]) -> bool:
        """
        Check if another bounds or value object is a subset of this range.

        The other object must also be an Integer and its lower and upper bound must *both*
        be within the range of this bounds object.

        Parameters
        ----------
        bounds: BaseBounds or BaseValue
            Other bounds or value object to check.  If it's a Value object, check against
            the smallest compatible bounds, as returned by the Value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

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

    def union(self,
              *others: Union[IntegerBoundsType, IntegerValueType]
              ) -> IntegerBoundsType:
        """
        Return the union of this bounds and other bounds.

        The others list must also be Integer Bounds or Values.

        Parameters
        ----------
        others: IntegerBounds or ~gemd.entity.value.integer_value.IntegerValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

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

    def update(self, *others: Union[IntegerBoundsType, IntegerValueType]):
        """
        Update this bounds to include other bounds.

        The others list must also be Integer Bounds or Values.

        Parameters
        ----------
        others: IntegerBounds or ~gemd.entity.value.integer_value.IntegerValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        """
        result = self.union(*others)
        self.lower_bound = result.lower_bound
        self.upper_bound = result.upper_bound

"""Bound a real number to be between two values."""
from math import isfinite
from typing import TypeVar, Union

from gemd.entity.bounds.base_bounds import BaseBounds
import gemd.units as units

__all__ = ["RealBounds"]
RealBoundsType = TypeVar("RealBoundsType", bound="RealBounds")
BaseValueType = TypeVar("BaseValueType", bound="BaseValue")  # noqa: F821
ContinuousValueType = TypeVar("ContinuousValueType", bound="ContinuousValue")  # noqa: F821


class RealBounds(BaseBounds, typ="real_bounds"):
    """
    Bounded subset of the real numbers, parameterized by a lower and upper bound.

    Parameters
    ----------
    lower_bound: float
        The lower endpoint (inclusive) of the permitted range.
    upper_bound: float
        The upper endpoint (inclusive) of the permitted range.
    """

    def __init__(self, lower_bound: float, upper_bound: float, default_units: str):
        self._default_units = None
        self._lower_bound = None
        self._upper_bound = None

        self.default_units = default_units
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @property
    def lower_bound(self) -> float:
        """The lower endpoint of the permitted range."""
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value: float):
        """Set the lower endpoint of the permitted range."""
        if value is None or not isfinite(value):
            raise ValueError(f"Lower bound must be given and finite: {value}")
        if self.upper_bound is not None and value > self.upper_bound:
            raise ValueError(f"Upper bound ({self.upper_bound}) must be "
                             f"greater than or equal to lower bound ({value})")
        self._lower_bound = float(value)

    @property
    def upper_bound(self) -> float:
        """The upper endpoint of the permitted range."""
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, value: float):
        """Set the upper endpoint of the permitted range."""
        if value is None or not isfinite(value):
            raise ValueError(f"Upper bound must be given and finite: {value}")
        if self.lower_bound is not None and value < self.lower_bound:
            raise ValueError(f"Upper bound ({value}) must be "
                             f"greater than or equal to lower bound ({self.lower_bound})")
        self._upper_bound = float(value)

    @property
    def default_units(self) -> str:
        """
        A string describing the units.

        Units must be present and parseable by Pint.
        An empty string can be used for the units of a dimensionless quantity.
        """
        return self._default_units

    @default_units.setter
    def default_units(self, default_units: str):
        """Set the string describing the units."""
        if default_units is None:
            raise ValueError("Real bounds must have units. "
                             "Use an empty string for a dimensionless quantity.")
        self._default_units = units.parse_units(default_units, return_unit=False)

    def contains(self, bounds: Union[BaseBounds, BaseValueType]) -> bool:
        """
        Check if another bounds or value object is a subset of this range.

        The other object must also be Real and its lower and upper bound must *both*
        be within the range of this bounds object.  Values that are unbounded
        distributions (e.g., Gaussian) are generally assumed to be truncated and
        logic around permissibility is delegated to the Value implementation.

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
        if not isinstance(bounds, RealBounds):
            return False

        lower, upper = self._convert_bounds(bounds.default_units)
        if lower is None:
            return False

        return bounds.lower_bound >= lower and bounds.upper_bound <= upper

    def union(self,
              *others: Union[RealBoundsType, ContinuousValueType]
              ) -> RealBoundsType:
        """
        Return the union of this bounds and other bounds.

        The others list must also be Real Bounds or Values.

        Parameters
        ----------
        others: RealBounds or ContinuousValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        Returns
        -------
        RealBounds
            The union of this bounds and the passed bounds

        """
        from gemd.entity.value.continuous_value import ContinuousValue

        if any(not isinstance(x, (RealBounds, ContinuousValue)) for x in others):
            misses = {type(x).__name__
                      for x in others
                      if not isinstance(x, (RealBounds, ContinuousValue))}
            raise TypeError(f"union requires consistent typing; expected real, found {misses}")
        lower = self.lower_bound
        upper = self.upper_bound
        unit_ = self.default_units
        for bounds in others:
            if isinstance(bounds, ContinuousValue):
                bounds: RealBounds = bounds._to_bounds()
            bnd_lo, bnd_hi = bounds._convert_bounds(unit_)
            if bnd_lo is None or bnd_hi is None:
                raise units.IncompatibleUnitsError(bounds.default_units, unit_)
            if bnd_lo < lower:
                lower = bnd_lo
            if bnd_hi > upper:
                upper = bnd_hi
        return RealBounds(lower_bound=lower, upper_bound=upper, default_units=unit_)

    def update(self, *others: Union[RealBoundsType, ContinuousValueType]):
        """
        Update this bounds to include other bounds.

        The others list must also be Real Bounds or Values.

        Parameters
        ----------
        others: RealBounds or ContinuousValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        """
        result = self.union(*others)
        self.lower_bound = result.lower_bound
        self.upper_bound = result.upper_bound
        self.default_units = result.default_units

    def _convert_bounds(self, target_units):
        """
        Convert the bounds to the target unit system, or None if not possible.

        Parameters
        ----------
        target_units: str
            The units to convert into.

        Returns
        -------
        tuple (float, float)
            A tuple of the (lower_bound, upper_bound) in the target units.

        """
        try:
            lower_bound = units.convert_units(
                self.lower_bound, self.default_units, target_units)
            upper_bound = units.convert_units(
                self.upper_bound, self.default_units, target_units)
            return lower_bound, upper_bound
        except units.IncompatibleUnitsError:
            return None, None

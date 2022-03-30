"""Base class for all bounds."""
from abc import abstractmethod
from typing import Union

import gemd.units as units
from gemd.entity.dict_serializable import DictSerializable

DIMENSIONLESS = "dimensionless"


class BaseBounds(DictSerializable):
    """Base class for bounds, including RealBounds and CategoricalBounds."""

    @abstractmethod
    def contains(self, bounds: Union["BaseBounds", "BaseValue"]):
        """
        Check if another bounds is contained within this bounds.

        Parameters
        ----------
        bounds: Union[BaseBounds, BaseValue]
            Other bounds object to check.  If it's a Value object, check against
            the smallest compatible bounds, as returned by the

        Returns
        -------
        bool
            True if any value that validates true for bounds also validates true for this

        """
        from gemd.entity.value.base_value import BaseValue

        if bounds is None:
            return False
        if isinstance(bounds, BaseValue):
            bounds = bounds._to_bounds()
        if isinstance(bounds, BaseBounds):
            return True
        raise TypeError('{} is not a Bounds object'.format(bounds))


def convert_bounds(lower_bound, upper_bound, source_units, target_units):
    """
    Convert the bounds to the target unit system, or None if not possible.

    Parameters
    ----------
    lower_bound: float
        Lower endpoint.
    upper_bound: float
        Upper endpoint.
    source_units: str
        A string describing the source units. Units must be present and they must
        be parseable by Pint. An empty string can be used for the units of a
        dimensionless quantity.
    target_units: str
        The units to convert into.

    Returns
    -------
    tuple (float, float)
        A tuple of the (lower_bound, upper_bound) in the target units.

    """
    try:
        lower_bound = units.convert_units(
            lower_bound, source_units, target_units)
        upper_bound = units.convert_units(
            upper_bound, source_units, target_units)
        return lower_bound, upper_bound
    except units.IncompatibleUnitsError:
        return None, None

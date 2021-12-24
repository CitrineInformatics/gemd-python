"""Base class for all continuous values."""
from gemd.entity.value.base_value import BaseValue
from gemd.units import parse_units
from gemd.entity.bounds import RealBounds

from abc import abstractmethod


class ContinuousValue(BaseValue):
    """
    A base class for values that correspond to a distribution over the real numbers.

    Parameters
    ----------
    units: str
        A string describing the units. Units must be present and they must be parseable by Pint.
        An empty string can be used for the units of a dimensionless quantity.

        Examples of acceptable units: 'm', 'meter', 'metre', 'm/s^2', 'degC', 'N/meter^2',
        'joule', 'J', 'dimensionless', ''.

        Examples of unacceptable units: 'JOULE'.

    """

    def __init__(self, units=None):
        self._units = None
        self.units = units

    @property
    def units(self) -> str:
        """Get the units of the value."""
        return self._units

    @units.setter
    def units(self, units: str):
        if units is None:
            raise ValueError("Continuous values must have units. "
                             "Use an empty string for a dimensionless quantity.")
        self._units = parse_units(units)

    @abstractmethod
    def _to_bounds(self) -> RealBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        RealBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.real_bounds.RealBounds>`.

        """

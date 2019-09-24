"""Base class for all continuous values."""
from taurus.entity.value.base_value import BaseValue
from taurus.units import parse_units


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

        Examples of unacceptable units: 'Joule', 'JOULE'.

    """

    def __init__(self, units=None):
        self._units = None
        self.units = units

    @property
    def units(self):
        """Get the units of the value."""
        return self._units

    @units.setter
    def units(self, units):
        if units is None:
            raise ValueError("Continuous values must have units. "
                             "Use an empty string for a dimensionless quantity.")
        self._units = parse_units(units)

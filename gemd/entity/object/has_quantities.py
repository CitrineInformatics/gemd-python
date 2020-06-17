"""For entities that hve quantities."""
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.value.continuous_value import ContinuousValue

fraction_bounds = RealBounds(lower_bound=0.0, upper_bound=1.0, default_units='')


class HasQuantities(object):
    """Mixin-trait that includes the mass, volume, number fraction, and absolute quantity."""

    def __init__(self, *,
                 mass_fraction=None, volume_fraction=None, number_fraction=None,
                 absolute_quantity=None):

        self._mass_fraction = None
        self.mass_fraction = mass_fraction

        self._volume_fraction = None
        self.volume_fraction = volume_fraction

        self._number_fraction = None
        self.number_fraction = number_fraction

        self._absolute_quantity = None
        self.absolute_quantity = absolute_quantity

    @property
    def mass_fraction(self):
        """Get mass fraction."""
        return self._mass_fraction

    @mass_fraction.setter
    def mass_fraction(self, mass_fraction):
        if mass_fraction is None:
            self._mass_fraction = None
        elif not isinstance(mass_fraction, ContinuousValue):
            raise TypeError("mass_fraction was not given as a continuous value")
        else:
            self._mass_fraction = mass_fraction

    @property
    def volume_fraction(self):
        """Get volume fraction."""
        return self._volume_fraction

    @volume_fraction.setter
    def volume_fraction(self, volume_fraction):
        if volume_fraction is None:
            self._volume_fraction = None
        elif not isinstance(volume_fraction, ContinuousValue):
            raise TypeError("volume_fraction was not given as a continuous value")
        else:
            self._volume_fraction = volume_fraction

    @property
    def number_fraction(self):
        """Get number fraction."""
        return self._number_fraction

    @number_fraction.setter
    def number_fraction(self, number_fraction):
        if number_fraction is None:
            self._number_fraction = None
        elif not isinstance(number_fraction, ContinuousValue):
            raise TypeError("number_fraction was not given as a continuous value")
        else:
            self._number_fraction = number_fraction

    @property
    def absolute_quantity(self):
        """Get absolute quantity."""
        return self._absolute_quantity

    @absolute_quantity.setter
    def absolute_quantity(self, absolute_quantity):
        if absolute_quantity is None:
            self._absolute_quantity = None
        elif isinstance(absolute_quantity, ContinuousValue):
            self._absolute_quantity = absolute_quantity
        else:
            raise TypeError("absolute_quantity was not given as a continuous value")

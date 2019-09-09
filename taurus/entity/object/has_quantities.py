"""For entities that hve quantities."""
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.value.continuous_value import ContinuousValue
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.entity.value.uniform_real import UniformReal

fraction_bounds = RealBounds(lower_bound=0.0, upper_bound=1.0, default_units='')


class HasQuantities(object):
    """Mixin-trait that includes the mass, volume, number fraction, and absolute quantity."""

    def __init__(self, mass_fraction=None, volume_fraction=None, number_fraction=None,
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
        if mass_fraction is not None and not fraction_bounds.validate(mass_fraction):
            raise ValueError("mass_fraction was not given as a fraction: {}".format(mass_fraction))
        self._mass_fraction = mass_fraction

    @property
    def volume_fraction(self):
        """Get volume fraction."""
        return self._volume_fraction

    @volume_fraction.setter
    def volume_fraction(self, volume_fraction):
        if volume_fraction is not None and not fraction_bounds.validate(volume_fraction):
            raise ValueError("volume_fraction was not given as a fraction")
        self._volume_fraction = volume_fraction

    @property
    def number_fraction(self):
        """Get number fraction."""
        return self._number_fraction

    @number_fraction.setter
    def number_fraction(self, number_fraction):
        if number_fraction is not None and not fraction_bounds.validate(number_fraction):
            raise ValueError("number_fraction was not given as a fraction")
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
            if isinstance(absolute_quantity, NominalReal) and absolute_quantity.nominal < 0:
                raise ValueError("absolute_quantity must be positive")
            elif isinstance(absolute_quantity, NormalReal) and absolute_quantity.mean < 0:
                raise ValueError("absolute_quantity must be positive")
            elif isinstance(absolute_quantity, UniformReal) and absolute_quantity.lower_bound < 0:
                raise ValueError("absolute_quantity must be positive")
            self._absolute_quantity = absolute_quantity
        else:
            raise TypeError("absolute_quantity was not given as a continuous value")

"""For entities that hve quantities."""
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.value.continuous_value import ContinuousValue
from gemd.entity.value.base_value import BaseValue
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger


class HasQuantities(object):
    """Mixin-trait that includes the mass, volume, number fraction, and absolute quantity.

    Parameters
    ----------
    mass_fraction: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The mass fraction of the quantity.
    volume_fraction: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The volume fraction of the quantity.
    number_fraction: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The number fraction of the quantity.
    absolute_quantity: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The absolute quantity of the quantity.

    """

    def __init__(self, *,
                 mass_fraction: ContinuousValue = None,
                 volume_fraction: ContinuousValue = None,
                 number_fraction: ContinuousValue = None,
                 absolute_quantity: ContinuousValue = None):

        self._mass_fraction = None
        self.mass_fraction = mass_fraction

        self._volume_fraction = None
        self.volume_fraction = volume_fraction

        self._number_fraction = None
        self.number_fraction = number_fraction

        self._absolute_quantity = None
        self.absolute_quantity = absolute_quantity

    @staticmethod
    def _check(value: BaseValue):
        fraction_bounds = RealBounds(lower_bound=0.0, upper_bound=1.0, default_units='')
        level = get_validation_level()
        accept = level == WarningLevel.IGNORE or fraction_bounds.contains(value)
        if not accept:
            message = f"Value {value} is not between 0 and 1."
            if level == WarningLevel.WARNING:
                logger.warning(message)
            else:
                raise ValueError(message)

    @property
    def mass_fraction(self) -> ContinuousValue:
        """Get mass fraction."""
        return self._mass_fraction

    @mass_fraction.setter
    def mass_fraction(self, mass_fraction: ContinuousValue):
        if mass_fraction is None:
            self._mass_fraction = None
        elif not isinstance(mass_fraction, ContinuousValue):
            raise TypeError("mass_fraction was not given as a continuous value")
        else:
            self._check(mass_fraction)
            self._mass_fraction = mass_fraction

    @property
    def volume_fraction(self) -> ContinuousValue:
        """Get volume fraction."""
        return self._volume_fraction

    @volume_fraction.setter
    def volume_fraction(self, volume_fraction: ContinuousValue):
        if volume_fraction is None:
            self._volume_fraction = None
        elif not isinstance(volume_fraction, ContinuousValue):
            raise TypeError("volume_fraction was not given as a continuous value")
        else:
            self._check(volume_fraction)
            self._volume_fraction = volume_fraction

    @property
    def number_fraction(self) -> ContinuousValue:
        """Get number fraction."""
        return self._number_fraction

    @number_fraction.setter
    def number_fraction(self, number_fraction: ContinuousValue):
        if number_fraction is None:
            self._number_fraction = None
        elif not isinstance(number_fraction, ContinuousValue):
            raise TypeError("number_fraction was not given as a continuous value")
        else:
            self._check(number_fraction)
            self._number_fraction = number_fraction

    @property
    def absolute_quantity(self) -> ContinuousValue:
        """Get absolute quantity."""
        return self._absolute_quantity

    @absolute_quantity.setter
    def absolute_quantity(self, absolute_quantity: ContinuousValue):
        if absolute_quantity is None:
            self._absolute_quantity = None
        elif isinstance(absolute_quantity, ContinuousValue):
            self._absolute_quantity = absolute_quantity
        else:
            raise TypeError("absolute_quantity was not given as a continuous value")

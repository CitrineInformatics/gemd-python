"""Base class for integer values."""
from gemd.entity.value.base_value import BaseValue
from gemd.entity.bounds import IntegerBounds

from abc import abstractmethod


class IntegerValue(BaseValue):
    """A base class for values that correspond to a distribution over the integers."""

    @abstractmethod
    def _to_bounds(self) -> IntegerBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        IntegerBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.integer_bounds.IntegerBounds>`.

        """

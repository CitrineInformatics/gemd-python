"""Base class for integer values."""
from gemd.entity.value.base_value import BaseValue
from gemd.entity.bounds import IntegerBounds

from abc import abstractmethod

__all__ = ["IntegerValue"]


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
            :class:`~gemd.entity.bounds.integer_bounds.IntegerBounds`.

        """

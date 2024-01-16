"""Composition of a material."""
from gemd.entity.value.base_value import BaseValue
from gemd.entity.bounds import CompositionBounds

from abc import abstractmethod

__all__ = ["CompositionValue"]


class CompositionValue(BaseValue):
    """Base class for composition values."""

    @abstractmethod
    def _to_bounds(self) -> CompositionBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        CompositionBounds
            The minimally consistent
            :class:`~gemd.entity.bounds.composition_bounds.CompositionBounds`.

        """

"""Base class for categorical values."""
from gemd.entity.value.base_value import BaseValue
from gemd.entity.bounds import CategoricalBounds

from abc import abstractmethod

__all__ = ["CategoricalValue"]


class CategoricalValue(BaseValue):
    """
    Base class for categorical values, which are distributions over valid category names.

    All category names must be in unicode.
    """

    @abstractmethod
    def _to_bounds(self) -> CategoricalBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        CategoricalBounds
            The minimally consistent
            :class:`gemd.entity.bounds.categorical_bounds.CategoricalBounds`.

        """

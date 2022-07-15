"""Base class for all bounds."""
from abc import abstractmethod
from typing import Union

from gemd.entity.dict_serializable import DictSerializable


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

    @abstractmethod
    def union(self, *others: Union["BaseBounds", "BaseValue"]) -> "BaseBounds":
        """
        Return the union of this bounds and other bounds.

        The others list must also be the same class (e.g., categorical, real...).

        Parameters
        ----------
        others: Union[BaseBounds, BaseValue]
            Other bounds or value objects to include.

        Returns
        -------
        BaseBounds
            The union of this bounds and the passed bounds

        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, *others: Union["BaseBounds", "BaseValue"]):
        """
        Update this bounds to include other bounds.

        The others list must also be the same class (e.g., categorical, real...).

        Parameters
        ----------
        others: Union[BaseBounds, BaseValue]
            Other bounds or value objects to include.

        """
        pass  # pragma: no cover

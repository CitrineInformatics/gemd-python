"""Base class for all bounds."""
from abc import abstractmethod
from typing import TypeVar, Union

from gemd.entity.dict_serializable import DictSerializable

__all__ = ["BaseBounds"]
BaseBoundsType = TypeVar("BaseBoundsType", bound="BaseBounds")
BaseValueType = TypeVar("BaseValueType", bound="BaseValue")  # noqa: F821


class BaseBounds(DictSerializable):
    """Base class for bounds, including RealBounds and CategoricalBounds."""

    @abstractmethod
    def contains(self, bounds: Union[BaseBoundsType, BaseValueType]):
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
    def union(self, *others: Union[BaseBoundsType, BaseValueType]) -> BaseBoundsType:
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

    @abstractmethod
    def update(self, *others: Union[BaseBoundsType, BaseValueType]):
        """
        Update this bounds to include other bounds.

        The others list must also be the same class (e.g., categorical, real...).

        Parameters
        ----------
        others: Union[BaseBounds, BaseValue]
            Other bounds or value objects to include.

        """
        pass  # pragma: no cover

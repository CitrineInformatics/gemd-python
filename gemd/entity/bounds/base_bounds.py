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
        bounds: BaseBounds or BaseValue
            Other bounds object to check.  If it's a Value object, check against
            the smallest compatible bounds, as returned by the Value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        Returns
        -------
        bool
            True if all values valid for `bounds` are also valid for this object

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
        others: BaseBounds or BaseValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

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
        others: BaseBounds or BaseValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        """

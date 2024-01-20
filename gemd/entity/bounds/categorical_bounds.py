from typing import TypeVar, Any, Union, Set, Optional, Iterable, Dict

from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.util import array_like

__all__ = ["CategoricalBounds"]
CategoricalBoundsType = TypeVar("CategoricalBoundsType", bound="CategoricalBounds")
BaseValueType = TypeVar("BaseValueType", bound="BaseValue")  # noqa: F821
CategoricalValueType = TypeVar("CategoricalValueType", bound="CategoricalValue")  # noqa: F821


class CategoricalBounds(BaseBounds, typ="categorical_bounds"):
    """
    Categorical bounds, parameterized by a set of string-valued category labels.

    Parameters
    ----------
    categories: list, tuple, or set of strings
        A collection of the allowed categories

    """

    def __init__(self, categories: Optional[Iterable[str]] = None):
        self._categories = None
        self.categories = categories

    @property
    def categories(self) -> Set[str]:
        """The collection of allowed categories."""
        return self._categories

    @categories.setter
    def categories(self, categories: Optional[Iterable[str]]):
        if categories is None:
            self._categories = set()
        elif isinstance(categories, array_like()):
            self._categories = set(categories)
        elif isinstance(categories, set):
            self._categories = categories
        else:
            raise ValueError("Categories must be a list, tuple, or set")

        if not all(isinstance(x, str) for x in self.categories):
            raise ValueError("All the categories must be strings")

    def contains(self, bounds: Union[BaseBounds, BaseValueType]) -> bool:
        """
        Check if another bounds object or value object is contained by this bounds.

        The other object must also be Categorical and its allowed categories must be a
        subset of this bounds's allowed categories.

        Parameters
        ----------
        bounds: BaseBounds or BaseValue
            Other bounds or value object to check.  If it's a Value object, check against
            the smallest compatible bounds, as returned by the Value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.


        Returns
        -------
        bool
            True if the other object is contained by this bounds.

        """
        from gemd.entity.value.base_value import BaseValue

        if not super().contains(bounds):
            return False
        if isinstance(bounds, BaseValue):
            bounds = bounds._to_bounds()
        if not isinstance(bounds, CategoricalBounds):
            return False

        return bounds.categories.issubset(self.categories)

    def union(self,
              *others: Union[CategoricalBoundsType, CategoricalValueType]
              ) -> CategoricalBoundsType:
        """
        Return the union of this bounds and other bounds.

        The others list must also be Categorical Bounds or Values.

        Parameters
        ----------
        others: CategoricalBounds or ~gemd.value.categorical_value.CategoricalValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        Returns
        -------
        CategoricalBounds
            The union of this bounds and the passed bounds

        """
        from gemd.entity.value.categorical_value import CategoricalValue

        if any(not isinstance(x, (CategoricalBounds, CategoricalValue)) for x in others):
            misses = {type(x).__name__
                      for x in others
                      if not isinstance(x, (CategoricalBounds, CategoricalValue))}
            raise TypeError(f"union requires consistent typing; "
                            f"expected categorical, found {misses}")
        result = self.categories.copy()
        for bounds in others:
            if isinstance(bounds, CategoricalValue):
                bounds = bounds._to_bounds()
            result.update(bounds.categories)
        return CategoricalBounds(result)

    def update(self, *others: Union[CategoricalBoundsType, CategoricalValueType]):
        """
        Update this bounds to include other bounds.

        The others list must also be Categorical Bounds or Values.

        Parameters
        ----------
        others: CategoricalBounds or ~gemd.entity.value.categorical_value.CategoricalValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        """
        self.categories = self.union(*others).categories

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert bounds to a dictionary.

        Returns
        -------
        dict
            A dictionary with "type" and "categories" (a sorted list of the categories).

        """
        return {"type": self.typ, "categories": sorted(list(self.categories))}

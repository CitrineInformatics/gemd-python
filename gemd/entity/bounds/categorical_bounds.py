"""A restricted set of categories."""
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.util import array_like

from typing import Union, Set, Optional, Iterable


class CategoricalBounds(BaseBounds):
    """
    Categorical bounds, parameterized by a set of string-valued category labels.

    Parameters
    ----------
    categories: list, tuple, or set of strings
        A collection of the allowed categories

    """

    typ = "categorical_bounds"

    def __init__(self, categories: Optional[Iterable[str]] = None):
        self._categories = None
        self.categories = categories

    @property
    def categories(self) -> Set[str]:
        """Get the set of categories."""
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

    def contains(self, bounds: Union[BaseBounds, "BaseValue"]) -> bool:
        """
        Check if another bounds object or value objects is contained by this bounds.

        The other object must also be Categorical and its allowed categories must be a
        subset of this bounds's allowed categories.

        Parameters
        ----------
        bounds: Union[BaseBounds, BaseValue]
            Other bounds or value object to check.

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
              *others: Union["CategoricalBounds", "CategoricalValue"]
              ) -> "CategoricalBounds":
        """
        Return the union of this bounds and other bounds.

        The others list must also be Categorical Bounds or Values.

        Parameters
        ----------
        others: Union[CategoricalBounds, CategoricalValue]
            Other bounds or value objects to include.

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

    def update(self, *others: Union["CategoricalBounds", "CategoricalValue"]):
        """
        Update this bounds to include other bounds.

        The others list must also be Categorical Bounds or Values.

        Parameters
        ----------
        others: Union[CategoricalBounds, CategoricalValue]
            Other bounds or value objects to include.

        """
        self.categories = self.union(*others).categories

    def as_dict(self):
        """
        Convert bounds to a dictionary.

        Returns
        -------
        dict
            A dictionary with "type" and "categories" (a sorted list of the categories).

        """
        return {"type": self.typ, "categories": sorted(list(self.categories))}

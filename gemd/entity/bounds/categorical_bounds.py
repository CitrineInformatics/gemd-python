"""A restricted set of categories."""
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.util import array_like

from typing import Union


class CategoricalBounds(BaseBounds):
    """
    Categorical bounds, parameterized by a set of string-valued category labels.

    Parameters
    ----------
    categories: list, tuple, or set of strings
        A collection of the allowed categories

    """

    typ = "categorical_bounds"

    def __init__(self, categories=None):
        self._categories = None
        self.categories = categories

    @property
    def categories(self):
        """Get the set of categories."""
        return self._categories

    @categories.setter
    def categories(self, categories):
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

    def as_dict(self):
        """
        Convert bounds to a dictionary.

        Returns
        -------
        dict
            A dictionary with "type" and "categories" (a sorted list of the categories).

        """
        return {"type": self.typ, "categories": sorted(list(self.categories))}

"""A restricted set of categories."""
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.util import array_like


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

    def contains(self, bounds: BaseBounds) -> bool:
        """
        Check if another bounds object is contained by this bounds.

        The other bounds must also be a CategoricalBounds and its allowed categories must be a
        subset of this bounds's allowed categories.

        Parameters
        ----------
        bounds: BaseBounds
            Other bounds object to check.

        Returns
        -------
        bool
            True if the other bounds is contained by this bounds.

        """
        if not super().contains(bounds):
            return False
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

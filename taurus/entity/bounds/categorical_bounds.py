"""A restricted set of categories."""
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.value.base_value import BaseValue
from taurus.entity.value.categorical_value import CategoricalValue
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_categorical import NominalCategorical
from taurus.entity.util import array_like


class CategoricalBounds(BaseBounds):
    """
    Categorical bounds, parameterized by a set of string-valued category labels.

    Parameters
    ----------
    categories: list, tuple, or set
        A collection of the allowed categories, each of which must be a string.

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

    def validate(self, value: BaseValue) -> bool:
        """
        Check if a value is in the set of allowed categories.

        Parameters
        ----------
        value: BaseValue
            Value to validate. In order to be valid, must be a
            :py:class:`CategoricalValue <taurus.entity.value.categorical_value.CategoricalValue>`

        Returns
        -------
        bool
            True if the value is one of the allowed categories.

        """
        if not super().validate(value):
            return False
        if not isinstance(value, CategoricalValue):
            return False

        if isinstance(value, DiscreteCategorical):
            return all(x in self.categories for x in value.probabilities)

        if isinstance(value, NominalCategorical):
            return value.category in self.categories

        msg = "Categorical bounds do not check every CategoricalValue subclass"  # pragma: no cover
        assert False, msg  # pragma: no cover

    def contains(self, bounds: BaseBounds) -> bool:
        """
        Check if another bounds object is contained by this bounds.

        The other bounds must also be a categorical and its allowed categories must be a subset
        of this bounds's allowed categories.

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
            A dictionary with "type" and "categories".

        """
        return {"type": self.typ, "categories": sorted(list(self.categories))}

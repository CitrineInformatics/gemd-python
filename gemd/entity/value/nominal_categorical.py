"""A value that nominally is equal to a single category."""
from gemd.entity.setters import validate_str
from gemd.entity.value.categorical_value import CategoricalValue
from gemd.entity.bounds import CategoricalBounds


class NominalCategorical(CategoricalValue):
    """
    A nominal category that the value is believe to have. It may not be exact.

    Parameters
    ----------
    category: str
        The nominal category.

    """

    typ = "nominal_categorical"

    def __init__(self, category=None):
        self._category = None
        self.category = category

    @property
    def category(self) -> str:
        """Get the category."""
        return self._category

    @category.setter
    def category(self, category: str):
        if category is None:
            self._category = None
        else:
            self._category = validate_str(category)

    def _to_bounds(self) -> CategoricalBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        BaseBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.categorical_bounds.CategoricalBounds>`.

        """
        return CategoricalBounds(categories={self.category})

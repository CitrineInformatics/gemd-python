"""A value that nominally is equal to a single category."""
from taurus.entity.setters import validate_str
from taurus.entity.value.categorical_value import CategoricalValue


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
    def category(self):
        """Get the category."""
        return self._category

    @category.setter
    def category(self, category):
        if category is None:
            self._category = None
        else:
            self._category = validate_str(category)

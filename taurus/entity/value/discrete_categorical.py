"""Discrete distribution across several categories."""
from toolz import keymap

from taurus.entity.setters import validate_str
from taurus.entity.value.categorical_value import CategoricalValue


class DiscreteCategorical(CategoricalValue):
    """
    Distribution over a discrete set of categories.

    Parameters
    ----------
    probabilities: str or Map[str, float]
        The categories and their probabilities.

        If a string is provided, that string corresponds to the only category and is given a
        probability of 1.0

        If a dictionary is provided, then each key is a category and its value is the probability
        of that category. The probabilities *must* sum to 1.0.

    """

    typ = "discrete_categorical"

    def __init__(self, probabilities=None):
        self._probabilities = None
        self.probabilities = probabilities

    @property
    def probabilities(self):
        """Get the map from categories to probabilities."""
        return self._probabilities

    @probabilities.setter
    def probabilities(self, probabilities):
        if probabilities is None:
            self._probabilities = None
        elif isinstance(probabilities, str):
            self._probabilities = {validate_str(probabilities): 1.0}
        elif isinstance(probabilities, dict):
            if abs(sum(probabilities.values()) - 1.0) > 1.0e-9:
                raise ValueError("probabilities must sum to 1.0")
            self._probabilities = keymap(validate_str, probabilities)
        else:
            raise TypeError("probabilities must be dict or single value")

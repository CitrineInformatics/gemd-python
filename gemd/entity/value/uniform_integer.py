"""A uniformly distributed integer value."""
from gemd.entity.value.integer_value import IntegerValue


class UniformInteger(IntegerValue):
    """
    Uniform integer distribution, with inclusive lower and upper bounds.

    Parameters
    ----------
    lower_bound: int
        Inclusive lower bound of the distribution.
    upper_bound: int
        Inclusive upper bound of the distribution.

    """

    typ = "uniform_integer"

    def __init__(self, lower_bound: int, upper_bound: int):
        self._lower_bound = None
        self._upper_bound = None

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        assert self.lower_bound <= self.upper_bound, \
            "the lower bound must be <= the upper bound"

    @property
    def lower_bound(self) -> int:
        """The lower bound of a uniform distribution."""
        return int(self._lower_bound)

    @lower_bound.setter
    def lower_bound(self, lower_bound: int) -> None:
        """The lower bound of a uniform distribution."""
        # This check is necessary to handle JSON serialization behavior under 3.5
        assert float(int(lower_bound)) == float(lower_bound), "lower bound must be an int"
        self._lower_bound = int(lower_bound)

    @property
    def upper_bound(self) -> int:
        """The upper bound of a uniform distribution."""
        return int(self._upper_bound)

    @upper_bound.setter
    def upper_bound(self, upper_bound: int) -> None:
        """The upper bound of a uniform distribution."""
        # This check is necessary to handle JSON serialization behavior under 3.5
        assert float(int(upper_bound)) == float(upper_bound), "upper bound must be an int"
        self._upper_bound = int(upper_bound)

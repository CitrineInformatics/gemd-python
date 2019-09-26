"""A uniformly distributed integer value."""
from taurus.entity.value.integer_value import IntegerValue


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

    def __init__(self, lower_bound=None, upper_bound=None):
        assert isinstance(lower_bound, int)
        assert isinstance(upper_bound, int)
        assert lower_bound <= upper_bound, \
            "the lower bound must be <= the upper bound"
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

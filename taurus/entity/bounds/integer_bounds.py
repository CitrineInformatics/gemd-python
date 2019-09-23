"""Bounds an integer to be between two values."""
from taurus.entity.bounds.base_bounds import BaseBounds


class IntegerBounds(BaseBounds):
    """
    Bounded subset of the integers, parameterized by a lower and upper bound.

    Parameters
    ----------
    lower_bound: int
        Lower endpoint.
    upper_bound: int
        Upper endpoint.

    """

    typ = "integer_bounds"

    def __init__(self, lower_bound=None, upper_bound=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        if self.lower_bound is None or abs(self.lower_bound) >= float("inf"):
            raise ValueError("Lower bound must be given and finite: {}".format(self.lower_bound))

        if self.upper_bound is None or abs(self.upper_bound) >= float("inf"):
            raise ValueError("Upper bound must be given and finite")

        if self.upper_bound < self.lower_bound:
            raise ValueError("Upper bound must be greater than or equal to lower bound")

    def contains(self, bounds: BaseBounds) -> bool:
        """
        Check if another bounds is a subset of this range.

        The other bounds must also be an IntegerBounds and its lower and upper bound must *both*
        be within the range of this bounds object.

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
        if not isinstance(bounds, IntegerBounds):
            return False

        return bounds.lower_bound >= self.lower_bound and bounds.upper_bound <= self.upper_bound

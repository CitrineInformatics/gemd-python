"""A uniformly distributed integer value."""
from gemd.entity.value.integer_value import IntegerValue
from gemd.entity.bounds import IntegerBounds


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

    @property
    def lower_bound(self) -> int:
        """The lower bound of a uniform distribution."""
        return int(self._lower_bound)

    @lower_bound.setter
    def lower_bound(self, lower_bound: int) -> None:
        """The lower bound of a uniform distribution."""
        # This check/cast is necessary to handle JSON serialization behavior under 3.6
        if not isinstance(lower_bound, (int, float)) or int(lower_bound) != lower_bound:
            raise TypeError(
                "lower_bound must be an int; got {}({})".format(type(lower_bound), lower_bound))
        if self._upper_bound is not None:
            if lower_bound > self.upper_bound:
                raise ValueError(
                    "lower_bound ({}) must be <= upper_bound ({})".format(lower_bound,
                                                                          self.upper_bound))
        self._lower_bound = int(lower_bound)

    @property
    def upper_bound(self) -> int:
        """The upper bound of a uniform distribution."""
        return int(self._upper_bound)

    @upper_bound.setter
    def upper_bound(self, upper_bound: int) -> None:
        """The upper bound of a uniform distribution."""
        # This check/cast is necessary to handle JSON serialization behavior under 3.6
        if not isinstance(upper_bound, (int, float)) or int(upper_bound) != upper_bound:
            raise TypeError(
                "upper_bound must be an int; got {}({})".format(type(upper_bound), upper_bound))
        if self.lower_bound > upper_bound:
            raise ValueError(
                "upper_bound ({}) must be >= lower_bound ({})".format(upper_bound,
                                                                      self.lower_bound))
        self._upper_bound = int(upper_bound)

    def _to_bounds(self) -> IntegerBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        IntegerBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.integer_bounds.IntegerBounds>`.

        """
        return IntegerBounds(lower_bound=self.lower_bound, upper_bound=self.upper_bound)

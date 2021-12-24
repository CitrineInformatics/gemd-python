"""A uniformly distributed real value."""
from gemd.entity.value.continuous_value import ContinuousValue
from gemd.entity.bounds import RealBounds


class UniformReal(ContinuousValue):
    """
    Uniform continuous distribution, with inclusive lower and upper bounds.

    Note
    ----
    These are especially useful for expressing uncertainty when the number of digits is
    truncated. For example, a measured value of 1.3 could be represented as a uniform real with
    a lower bound of 1.25 and an upper bound of 1.35.

    Parameters
    ----------
    lower_bound: float
        Inclusive lower bound of the distribution.
    upper_bound: float
        Inclusive upper bound of the distribution.
    units: str
        A string describing the units. Units must be present and they must be parseable by Pint.
        An empty string can be used for the units of a dimensionless quantity.

    """

    typ = "uniform_real"

    def __init__(self, lower_bound=None, upper_bound=None, units=None):
        ContinuousValue.__init__(self, units)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        assert lower_bound <= upper_bound, \
            "the lower bound must be <= the upper bound"

    def _to_bounds(self) -> RealBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        RealBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.real_bounds.RealBounds>`.

        """
        return RealBounds(lower_bound=self.lower_bound,
                          upper_bound=self.upper_bound,
                          default_units=self.units)

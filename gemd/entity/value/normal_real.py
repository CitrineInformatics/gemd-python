"""A normally distributed real value."""
from gemd.entity.value.continuous_value import ContinuousValue
from gemd.entity.bounds import RealBounds


class NormalReal(ContinuousValue):
    """
    Normal distribution over real numbers, parameterized by a mean and standard deviation.

    Parameters
    ----------
    mean: float
        Mean of the distribution.
    std: float
        Standard deviation of the normal distribution.
    units: str
        A string describing the units. Units must be present and they must be parseable by Pint.
        An empty string can be used for the units of a dimensionless quantity.

    """

    typ = "normal_real"

    def __init__(self, mean=None, std=None, units=None):
        ContinuousValue.__init__(self, units)
        self.mean = mean
        self.std = std

    def _to_bounds(self) -> RealBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        RealBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.real_bounds.RealBounds>`.

        """
        return RealBounds(lower_bound=self.mean,
                          upper_bound=self.mean,
                          default_units=self.units)

"""A normally distributed real value."""
from taurus.entity.value.continuous_value import ContinuousValue


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

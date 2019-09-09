"""A nominal real value."""
from taurus.entity.value.continuous_value import ContinuousValue


class NominalReal(ContinuousValue):
    """
    Nominal real, which does not specify an uncertainty but is not to be assumed exact.

    Parameters
    ----------
    nominal: float
        A nominal value--not assumed to be exact.
    units: str
        A string describing the units. Units must be present and they must be parseable by Pint.
        An empty string can be used for the units of a dimensionless quantity.

    """

    typ = "nominal_real"

    def __init__(self, nominal=None, units=None):
        ContinuousValue.__init__(self, units)
        assert isinstance(nominal, (int, float)), \
            "nominal value must be an int or float"
        self.nominal = float(nominal)

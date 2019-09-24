"""A nominal integer value."""
from taurus.entity.value.integer_value import IntegerValue


class NominalInteger(IntegerValue):
    """
    Nominal integer, which does not specify an uncertainty but is not assumed to be exact.

    Parameters
    ----------
    nominal: int
        A nominal value--not assumed to be exact.

    """

    typ = "nominal_integer"

    def __init__(self, nominal=None):
        assert isinstance(nominal, int), \
            "nominal value must be an int"
        self.nominal = nominal

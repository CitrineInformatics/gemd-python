"""A nominal integer value."""
from gemd.entity.value.integer_value import IntegerValue


class NominalInteger(IntegerValue):
    """
    Nominal integer, which does not specify an uncertainty but is not assumed to be exact.

    Parameters
    ----------
    nominal: int
        A nominal value--not assumed to be exact.

    """

    typ = "nominal_integer"

    def __init__(self, nominal):
        self._nominal = None
        self.nominal = nominal

    @property
    def nominal(self) -> int:
        """A proscribed integer value without uncertainty."""
        return int(self._nominal)

    @nominal.setter
    def nominal(self, nominal: int) -> None:
        """A proscribed integer value without uncertainty."""
        # This check is necessary to handle JSON serialization behavior under 3.5
        assert float(int(nominal)) == float(nominal), "nominal value must be an int"
        self._nominal = int(nominal)

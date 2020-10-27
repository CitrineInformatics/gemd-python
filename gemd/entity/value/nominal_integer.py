"""A nominal integer value."""
from gemd.entity.value.integer_value import IntegerValue
from gemd.entity.bounds import IntegerBounds


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
        # This check/cast is necessary to handle JSON serialization behavior under 3.6
        if not isinstance(nominal, (int, float)) or int(nominal) != nominal:
            raise TypeError("nominal must be an int; got an {}({})".format(type(nominal), nominal))

        self._nominal = int(nominal)

    def _to_bounds(self) -> IntegerBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        IntegerBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.integer_bounds.IntegerBounds>`.

        """
        return IntegerBounds(lower_bound=self.nominal, upper_bound=self.nominal)

"""A nominal composition value."""
from gemd.entity.value.composition_value import CompositionValue
from gemd.entity.bounds import CompositionBounds


class NominalComposition(CompositionValue):
    """
    Nominal composition, represented as a map from the component names to the quantities.

    The quantities do not express an uncertainty but also do not imply that there is absolute
    certainty to their values.

    Parameters
    ----------
    quantities: Map[String, Number]
        A map from each component to its amount.  The quantities are not required to be expressed
        on a unit or fractional basis. The following are all acceptable:

        * dict(acetone=0.25, methanol=0.75)
        * dict(acetone=1, methanol=3)
        * dict(acetone=3.5, methanol=10.5)

    """

    typ = "nominal_composition"

    def __init__(self, quantities=None):
        self._quantities = None
        self.quantities = quantities

    @property
    def quantities(self) -> dict:
        """Get a map from the components to their quantities."""
        return self._quantities

    @quantities.setter
    def quantities(self, quantities: dict):
        if quantities is None:
            self._quantities = {}
        elif isinstance(quantities, dict):
            self._quantities = quantities
        elif isinstance(quantities, list):
            self._quantities = dict(quantities)
        else:
            raise TypeError("quantities must be dict or List of two-item lists or None")

    def _to_bounds(self) -> CompositionBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        BaseBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.categorical_bounds.CategoricalBounds>`.

        """
        return CompositionBounds(components=set(self.quantities))

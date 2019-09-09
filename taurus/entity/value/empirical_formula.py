"""An empirical chemical formaula."""
from typing import Dict

from taurus.entity.value.composition_value import CompositionValue
from pymatgen.core.composition import Composition as ElementalComposition
from pymatgen.core.composition import Element


class EmpiricalFormula(CompositionValue):
    """
    An empirical chemical formula where only the relative stoichiometries matter.

    Parameters
    ----------
    formula: str
        A string corresponding to the chemical formula of the composition.
        It must be parseable by pymatgen. The order and grouping of the elements is ignored.

    """

    typ = "empirical_formula"
    skip = {"_quantities"}

    def __init__(self, formula=None):
        self._formula = None
        self._quantities = None
        self.formula = formula

    @property
    def formula(self):
        """Get the formula as a string."""
        return self._formula

    @formula.setter
    def formula(self, value):
        self._quantities = self._parse_formula(value)
        self._formula = value

    @staticmethod
    def _parse_formula(formula_str) -> Dict[str, float]:
        """Parse the formula (a string) to return a map from elements to amounts."""
        return ElementalComposition(formula_str).to_reduced_dict

    @property
    def components(self):
        """Get all components of the chemical formula."""
        return self._quantities.keys()

    @property
    def quantities(self):
        """Get a map from components to quantities."""
        return self._quantities

    @staticmethod
    def all_elements():
        """The set of all elements in the periodic table."""
        return {e.value for e in Element}

"""An empirical chemical formaula."""
from gemd.entity.value.composition_value import CompositionValue
from gemd.entity.bounds import CompositionBounds


_all_elements = {
    'Tb', 'Be', 'Sb', 'Re', 'Sr', 'Ac', 'Ho', 'Ir', 'Cr', 'Os', 'S', 'Pt', 'Si', 'C', 'V', 'Bi',
    'U', 'Pr', 'B', 'O', 'Zn', 'Xe', 'N', 'Ni', 'No', 'Ti', 'Pa', 'Am', 'Cu', 'I', 'Al', 'Ba',
    'Pu', 'Ca', 'Bk', 'Ge', 'In', 'H', 'Es', 'Se', 'Cs', 'Te', 'Rn', 'Hf', 'Cm', 'Kr', 'Y',
    'Cf', 'Li', 'F', 'Hg', 'Sm', 'Nd', 'Br', 'Er', 'K', 'Zr', 'Pd', 'Au', 'Eu', 'Md', 'Ga', 'As',
    'Mn', 'Ag', 'Nb', 'Gd', 'Ru', 'Po', 'W', 'Na', 'Cl', 'Mo', 'Rh', 'Pm', 'Rb', 'Np', 'Lr',
    'Ce', 'Ra', 'Tm', 'Dy', 'Fr', 'Sc', 'Lu', 'Fe', 'Fm', 'Cd', 'Ar', 'Mg', 'P', 'Th', 'Co',
    'Tc', 'Pb', 'Ta', 'Tl', 'At', 'He', 'Yb', 'La', 'Sn', 'Ne'
}


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

    def __init__(self, formula=None):
        self._formula = None
        self.formula = formula

    @property
    def formula(self) -> str:
        """Get the formula as a string."""
        return self._formula

    @staticmethod
    def _elements(value: str):
        import re
        return set(re.findall('[A-Z][a-z]*', value))

    @formula.setter
    def formula(self, value: str):
        if value is None:
            self._formula = None
        elif isinstance(value, str):
            if not EmpiricalFormula._elements(value).issubset(_all_elements):
                unknown = sorted(EmpiricalFormula._elements(value).difference(_all_elements))
                raise ValueError('Formula {} contains unknown elements: {}'
                                 .format(value, ' '.join(unknown)))
            self._formula = value
        else:
            raise TypeError("Formula must be given as a string; got {}".format(type(value)))

    def _to_bounds(self) -> CompositionBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        BaseBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.categorical_bounds.CategoricalBounds>`.

        """
        return CompositionBounds(components=EmpiricalFormula._elements(self.formula))

    @staticmethod
    def all_elements() -> set:
        """The set of all elements in the periodic table."""
        return _all_elements

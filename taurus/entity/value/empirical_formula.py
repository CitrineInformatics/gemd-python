"""An empirical chemical formaula."""
from taurus.entity.value.composition_value import CompositionValue


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
    def formula(self):
        """Get the formula as a string."""
        return self._formula

    @formula.setter
    def formula(self, value):
        if value is None:
            self._formula = None
        elif isinstance(value, str):
            self._formula = value
        else:
            raise TypeError("Formula must be given as a string; got {}".format(type(value)))

    @staticmethod
    def all_elements():
        """The set of all elements in the periodic table."""
        return _all_elements

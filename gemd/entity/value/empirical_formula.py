"""An empirical chemical formula."""
import re

from gemd.entity.value.composition_value import CompositionValue
from gemd.entity.bounds import CompositionBounds

__all__ = ["EmpiricalFormula"]


_periodic_table = """
H   D   T                                                           He
Li  Be                                          B   C   N   O   F   Ne
Na  Mg                                          Al  Si  P   S   Cl  Ar
K   Ca  Sc  Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr
Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe
Cs  Ba      Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn
Fr  Ra      Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og

La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu
Ac  Th  Pa  U   Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr
"""
_all_elements = re.split(r"\s+", _periodic_table.strip())


class EmpiricalFormula(CompositionValue, typ="empirical_formula"):
    """
    An empirical chemical formula where only the relative stoichiometries matter.

    Parameters
    ----------
    formula: str
        A string corresponding to the chemical formula of the composition.
        It must be parseable by pymatgen. The order and grouping of the elements is ignored.

    """

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
            :class:`~gemd.entity.bounds.categorical_bounds.CategoricalBounds`.

        """
        return CompositionBounds(components=EmpiricalFormula._elements(self.formula))

    @staticmethod
    def all_elements() -> set:
        """The set of all elements in the periodic table."""
        return _all_elements

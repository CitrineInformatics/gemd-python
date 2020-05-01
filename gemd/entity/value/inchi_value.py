"""An empirical chemical formaula."""
from gemd.entity.value.molecular_value import MolecularValue


class InChI(MolecularValue):
    """
    A molecular structure encoded according to the IUPAC International Chemical Identifier (InChI).

    Parameters
    ----------
    inchi: str
        A string formatted according to the InChI standard.

    """

    typ = "inchi"

    def __init__(self, inchi=None):
        self._inchi = None
        self.inchi = inchi

    @property
    def inchi(self):
        """Get the formula as a string."""
        return self._inchi

    @inchi.setter
    def inchi(self, value):
        if value is None:
            self._inchi = None
        elif isinstance(value, str):
            self._inchi = value
        else:
            raise TypeError("InChI must be given as a string; got {}".format(type(value)))

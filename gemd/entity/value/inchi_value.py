"""An empirical chemical formaula."""
from gemd.entity.value.molecular_value import MolecularValue
from gemd.entity.bounds import MolecularStructureBounds


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
    def inchi(self) -> str:
        """Get the formula as a string."""
        return self._inchi

    @inchi.setter
    def inchi(self, value: str):
        if value is None:
            self._inchi = None
        elif isinstance(value, str):
            self._inchi = value
        else:
            raise TypeError("InChI must be given as a string; got {}".format(type(value)))

    def _to_bounds(self) -> MolecularStructureBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        MolecularStructureBounds
            The minimally consistent
            :class:`bounds
            <gemd.entity.bounds.molecular_structure_bounds.MolecularStructureBounds>`.

        """
        return MolecularStructureBounds()

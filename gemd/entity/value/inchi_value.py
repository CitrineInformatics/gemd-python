"""An empirical chemical formula."""

from gemd.entity.bounds import MolecularStructureBounds
from gemd.entity.value.molecular_value import MolecularValue

__all__ = ["InChI"]


class InChI(MolecularValue, typ="inchi"):
    """A molecular structure in IUPAC International Chemical Identifier (InChI) format.

    Parameters
    ----------
    inchi: str
        A string formatted according to the InChI standard.

    """

    def __init__(self, inchi=None):
        self._inchi = None
        self.inchi = inchi

    @property
    def inchi(self) -> str:
        """Get the InChI as a string."""
        return self._inchi

    @inchi.setter
    def inchi(self, value: str):
        """Set the InChI, correcting for some minor variations in format."""
        if value is None:
            self._inchi = None
        elif isinstance(value, str):
            if value.lower().startswith("1s/"):
                value = value.replace(value[:2], "InChI=1S")
            elif not value.lower().startswith("inchi"):
                value = f"InChI=1S/{value}"
            elif not value.startswith("InChI"):
                value = value.replace(value[:5], "InChI")
            self._inchi = value
        else:
            raise TypeError(f"InChI must be given as a string; got {type(value)}")

    def _to_bounds(self) -> MolecularStructureBounds:
        """Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        MolecularStructureBounds
            The minimally consistent
            :class:`~gemd.entity.bounds.molecular_structure_bounds.MolecularStructureBounds`.

        """
        return MolecularStructureBounds()

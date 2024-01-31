"""An empirical chemical formula."""
from gemd.entity.value.molecular_value import MolecularValue
from gemd.entity.bounds import MolecularStructureBounds

__all__ = ["Smiles"]


class Smiles(MolecularValue, typ="smiles"):
    """
    A molecular structure encoded according to SMILES.

    Parameters
    ----------
    smiles: str
        A string formatted according to the Simplified molecular-input line-entry system
        (SMILES) informal standard.

    """

    def __init__(self, smiles=None):
        self._smiles = None
        self.smiles = smiles

    @property
    def smiles(self) -> str:
        """Get the formula as a string."""
        return self._smiles

    @smiles.setter
    def smiles(self, value: str):
        if value is None:
            self._smiles = None
        elif isinstance(value, str):
            self._smiles = value
        else:
            raise TypeError("SMILES must be given as a string; got {}".format(type(value)))

    def _to_bounds(self) -> MolecularStructureBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        MolecularStructureBounds
            The minimally consistent
            :class:`~gemd.entity.bounds.molecular_structure_bounds.MolecularStructureBounds`.

        """
        return MolecularStructureBounds()

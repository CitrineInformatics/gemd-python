"""An empirical chemical formaula."""
from gemd.entity.value.molecular_value import MolecularValue


class Smiles(MolecularValue):
    """
    A molecular structure encoded according to SMILES.

    Parameters
    ----------
    smiles: str
        A string formatted according to the Simplified molecular-input line-entry system
        (SMILES) informal standard.

    """

    typ = "smiles"

    def __init__(self, smiles=None):
        self._smiles = None
        self.smiles = smiles

    @property
    def smiles(self):
        """Get the formula as a string."""
        return self._smiles

    @smiles.setter
    def smiles(self, value):
        if value is None:
            self._smiles = None
        elif isinstance(value, str):
            self._smiles = value
        else:
            raise TypeError("SMILES must be given as a string; got {}".format(type(value)))

"""
Bounds a molecular structure to be a valid representation.

In the future, this may include substructural restrictions.
"""
from gemd.entity.bounds.base_bounds import BaseBounds


class MolecularStructureBounds(BaseBounds):
    """Molecular bounds, with no component or substructural restrictions (yet)."""

    typ = "molecular_structure_bounds"

    def __init__(self):
        pass

    def contains(self, bounds: BaseBounds) -> bool:
        """
        Check if another bounds is contained by this bounds.

        The other bounds must also be a MolecularBounds.  There are no other
        conditions at this time.

        Parameters
        ----------
        bounds: BaseBounds
            Other bounds object to check.

        Returns
        -------
        bool
            True if the other bounds is contained by this bounds.

        """
        if not super().contains(bounds):
            return False
        if not isinstance(bounds, MolecularStructureBounds):
            return False

        return True

    def as_dict(self):
        """
        Convert bounds to a dictionary.

        Returns
        -------
        dict
            A dictionary with "type".

        """
        return {"type": self.typ}

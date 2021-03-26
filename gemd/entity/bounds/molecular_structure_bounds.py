"""
Bounds a molecular structure to be a valid representation.

In the future, this may include substructural restrictions.
"""
from gemd.entity.bounds.base_bounds import BaseBounds

from typing import Union


class MolecularStructureBounds(BaseBounds):
    """Molecular bounds, with no component or substructural restrictions (yet)."""

    typ = "molecular_structure_bounds"

    def __init__(self):
        pass

    def contains(self, bounds: Union[BaseBounds, "BaseValue"]) -> bool:
        """
        Check if another bounds or value object is contained by this bounds.

        The other object must also be or type Molecular.  There are no other
        conditions at this time.

        Parameters
        ----------
        bounds: Union[BaseBounds, BaseValue]
            Other bounds or value object to check.

        Returns
        -------
        bool
            True if the other bounds is contained by this bounds.

        """
        from gemd.entity.value.base_value import BaseValue

        if not super().contains(bounds):
            return False
        if isinstance(bounds, BaseValue):
            bounds = bounds._to_bounds()
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

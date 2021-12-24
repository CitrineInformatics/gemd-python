"""Composition of a material."""
from gemd.entity.value.base_value import BaseValue
from gemd.entity.bounds import MolecularStructureBounds

from abc import abstractmethod


class MolecularValue(BaseValue):
    """Base class for molecular structure values."""

    @abstractmethod
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

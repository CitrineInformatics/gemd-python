"""
Bounds a molecular structure to be a valid representation.

In the future, this may include substructural restrictions.
"""
from gemd.entity.bounds.base_bounds import BaseBounds

from typing import TypeVar, Union

__all__ = ["MolecularStructureBounds"]
MolecularBoundsType = TypeVar("MolecularBoundsType", bound="MolecularStructureBounds")
BaseValueType = TypeVar("BaseValueType", bound="BaseValue")  # noqa: F821
MolecularValueType = TypeVar("MolecularValueType", bound="MolecularValue")  # noqa: F821


class MolecularStructureBounds(BaseBounds, typ="molecular_structure_bounds"):
    """Molecular bounds, with no component or substructural restrictions (yet)."""

    def contains(self, bounds: Union[BaseBounds, BaseValueType]) -> bool:
        """
        Check if another bounds or value object is contained by this bounds.

        The other object must also be or type Molecular.  There are no other
        conditions at this time.

        Parameters
        ----------
        bounds: BaseBounds or BaseValue
            Other bounds or value object to check.  If it's a Value object, check against
            the smallest compatible bounds, as returned by the Value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

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

    def union(self,
              *others: Union[MolecularBoundsType, MolecularValueType]
              ) -> MolecularBoundsType:
        """
        Return the union of this bounds and other bounds.

        The others list must also be Molecular Structure Bounds or Values.

        Parameters
        ----------
        others: MolecularStructureBounds or ~gemd.entity.value.molecular_value.MolecularValue
            Other bounds or value objects to include.

        Returns
        -------
        MolecularStructureBounds
            The union of this bounds and the passed bounds.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        """
        from gemd.entity.value.molecular_value import MolecularValue

        if any(not isinstance(x, (MolecularStructureBounds, MolecularValue)) for x in others):
            misses = {type(x).__name__
                      for x in others
                      if not isinstance(x, (MolecularStructureBounds, MolecularValue))}
            raise TypeError(f"union requires consistent typing; "
                            f"expected molecular structure, found {misses}")
        return MolecularStructureBounds()

    def update(self, *others: Union[MolecularBoundsType, MolecularValueType]):
        """
        Update this bounds to include other bounds.

        The others list must also be Molecular Structure Bounds or Values.

        Parameters
        ----------
        others: MolecularStructureBounds or ~gemd.entity.value.molecular_value.MolecularValue
            Other bounds or value objects to include.  If they're Value objects,
            increase by the smallest compatible bounds, as returned by the value's
            :func:`~gemd.entity.base_bounds.BaseBounds._to_bounds` method.

        """
        pass  # This is a no-op for Molecular structure

    def as_dict(self):
        """
        Convert bounds to a dictionary.

        Returns
        -------
        dict
            A dictionary with "type".

        """
        return {"type": self.typ}

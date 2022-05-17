"""For entities that have specs."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.object.base_object import BaseObject
from gemd.entity.link_by_uid import LinkByUID

from abc import ABC, abstractmethod
from typing import Union, Set


class HasMaterial(HasDependencies, ABC):
    """Mix-in trait for objects that can be assigned materials."""

    @property
    @abstractmethod
    def material(self) -> Union[BaseObject, LinkByUID]:
        """Get the material."""

    @material.setter
    @abstractmethod
    def material(self, spec: Union[BaseObject, LinkByUID]):
        """Set the material."""

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.material} if self.material is not None else set()

"""For entities that have specs."""

from abc import ABC, abstractmethod

from gemd.entity.base_entity import BaseEntity
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.object.base_object import BaseObject

__all__ = ["HasMaterial"]


class HasMaterial(HasDependencies, ABC):
    """Mix-in trait for objects that can be assigned materials."""

    @property
    @abstractmethod
    def material(self) -> BaseObject | LinkByUID:
        """Get the material."""

    @material.setter
    @abstractmethod
    def material(self, spec: BaseObject | LinkByUID):
        """Set the material."""

    def _local_dependencies(self) -> set[BaseEntity | LinkByUID]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.material} if self.material is not None else set()

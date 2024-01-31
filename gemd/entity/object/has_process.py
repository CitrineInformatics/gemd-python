"""For entities that have specs."""
from gemd.entity.base_entity import BaseEntity
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.object.base_object import BaseObject

from abc import abstractmethod
from typing import Union, Set

__all__ = ["HasProcess"]


class HasProcess(HasDependencies):
    """Mix-in trait for objects that can be assigned materials."""

    @property
    @abstractmethod
    def process(self) -> Union[BaseObject, LinkByUID]:
        """Get the process."""

    @process.setter
    @abstractmethod
    def process(self, process: Union[BaseObject, LinkByUID]):
        """Set the process."""

    def _local_dependencies(self) -> Set[Union[BaseEntity, LinkByUID]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.process} if self.process is not None else set()

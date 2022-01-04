"""For entities that have dependencies."""
from abc import ABC, abstractmethod
from typing import Union, Set


class HasDependencies(ABC):
    """Mix-in trait for objects that reference other objects."""

    @abstractmethod
    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """All dependencies (objects) that this class introduces."""

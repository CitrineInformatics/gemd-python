"""For entities that have dependencies."""
from abc import ABC, abstractmethod
from typing import Union, Set

__all__ = ["HasDependencies"]


class HasDependencies(ABC):
    """Mix-in trait for objects that reference other objects."""

    @abstractmethod
    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:  # noqa: F821
        """All dependencies (objects) that this class introduces."""

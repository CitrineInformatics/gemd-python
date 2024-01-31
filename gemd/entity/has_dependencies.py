"""For entities that have dependencies."""
from abc import ABC, abstractmethod
from typing import TypeVar, Union, Set

__all__ = ["HasDependencies"]
BaseEntityType = TypeVar("BaseEntityType", bound="BaseEntity")  # noqa: F821
LinkByUIDType = TypeVar("LinkByUIDType", bound="LinkByUID")  # noqa: F821


class HasDependencies(ABC):
    """Mix-in trait for objects that reference other objects."""

    @abstractmethod
    def _local_dependencies(self) -> Set[Union[BaseEntityType, LinkByUIDType]]:
        """All dependencies (objects) that this class introduces."""

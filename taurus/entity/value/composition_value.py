"""Composition of a material."""
from abc import abstractmethod

from taurus.entity.value.base_value import BaseValue


class CompositionValue(BaseValue):
    """Base class for composition values."""

    @property
    @abstractmethod
    def components(self):
        """Get the components in the composition."""
        ...

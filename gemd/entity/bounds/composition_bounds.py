"""Bounds a composition to have a specified set of components."""
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.util import array_like

from typing import Union


class CompositionBounds(BaseBounds):
    """
    Composition bounds, parameterized by a set of string-valued category labels.

    Parameters
    ----------
    components: list, tuple, or set or strings
        A collection of the components that must be present in the composition.

    """

    typ = "composition_bounds"

    def __init__(self, components=None):
        self._components = None
        self.components = components

    @property
    def components(self):
        """Get the allowed components."""
        return self._components

    @components.setter
    def components(self, value):
        if value is None:
            self._components = set()
        elif isinstance(value, array_like()):
            self._components = set(value)
        elif isinstance(value, set):
            self._components = value
        else:
            raise ValueError("Components must be a list, tuple, or set: {}".format(value))

        if not all(isinstance(x, str) for x in self.components):
            raise ValueError("All the components must be strings")

    def contains(self, bounds: Union[BaseBounds, "BaseValue"]) -> bool:
        """
        Check if another bounds or value object is contained by this bounds.

        The other object must also be a Composition and its components must be a subset of
        this bounds's set of allowed components.

        Parameters
        ----------
        bounds: Union[BaseBounds, BaseValue]
            Other object to check.

        Returns
        -------
        bool
            True if the other object is contained by this bounds.

        """
        from gemd.entity.value.base_value import BaseValue

        if not super().contains(bounds):
            return False
        if isinstance(bounds, BaseValue):
            bounds = bounds._to_bounds()
        if not isinstance(bounds, CompositionBounds):
            return False

        return bounds.components.issubset(self.components)

    def as_dict(self):
        """
        Convert bounds to a dictionary.

        Returns
        -------
        dict
            A dictionary with "type" and "components" (a sorted list of the components).

        """
        return {"type": self.typ, "components": sorted(list(self.components))}

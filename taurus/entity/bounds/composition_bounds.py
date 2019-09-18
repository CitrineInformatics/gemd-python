"""Bounds a composition to have a specified set of components."""
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.value.base_value import BaseValue
from taurus.entity.value.composition_value import CompositionValue
from taurus.entity.util import array_like


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

    def validate(self, value: BaseValue) -> bool:
        """
        Check if a value has all of the required components.

        Parameters
        ----------
        value: BaseValue
            Value to validate. In order to be valid, must be a
            :py:class:`CompositionValue <taurus.entity.value.composition_value.CompositionValue>`
            and have all of the required components.

        Returns
        -------
        bool
            True if the value is a composition with all required components.
        """
        if not super().validate(value):
            return False
        if not isinstance(value, CompositionValue):
            return False

        return all(x in self.components for x in value.components)

    def contains(self, bounds: BaseBounds) -> bool:
        """
        Check if another bounds is contained by this bounds.

        The other bounds must also be a CompositionBounds and its components must be a subset of
        this bounds's set of required components.

        Parameters
        ----------
        bounds: BaseBounds
            Other bounds object to check.

        Returns
        -------
        bool
            True if the other bounds is contained by this bounds.

        """
        if not super().contains(bounds):
            return False
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

"""Attribute templates."""
from gemd.entity.base_entity import BaseEntity
from gemd.entity.bounds.base_bounds import BaseBounds

__all__ = ["AttributeTemplate"]


class AttributeTemplate(BaseEntity):
    """
    An attribute template, which can be a property, parameter, or condition template.

    Parameters
    ----------
    name: str, required
        The name of the attribute template.
    bounds: ~gemd.entity.bounds.base_bounds.BaseBounds
        Bounds circumscribe the values that are valid according to this attribute template.
    description: str, optional
        A long-form description of the attribute template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.

    """

    def __init__(self, name, *, description=None, bounds=None, uids=None, tags=None):
        BaseEntity.__init__(self, uids, tags)
        self.name = name
        self.description = description

        if not isinstance(name, str):
            raise ValueError("name must be a string")

        self._bounds = None
        self.bounds = bounds

    @property
    def bounds(self):
        """Bounds circumscribe the values that are valid according to this attribute template."""
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        """Set the bounds."""
        if bounds is None:
            raise ValueError(f"Bounds are required on {type(self).__name__}s")
        if not isinstance(bounds, BaseBounds):
            raise TypeError(f"Bounds must be an instance of BaseBounds: {bounds}")
        self._bounds = bounds

    def all_dependencies(self):
        """Return a set of all immediate dependencies (no recursion)."""
        # Attribute Templates never depend on other objects.
        return set()

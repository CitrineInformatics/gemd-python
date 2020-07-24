"""Attribute templates."""
from gemd.entity.base_entity import BaseEntity
from gemd.entity.bounds.base_bounds import BaseBounds


class AttributeTemplate(BaseEntity):
    """
    An attribute template, which can be a property, parameter, or condition template.

    Parameters
    ----------
    name: str, required
        The name of the attribute template.
    bounds: :py:class:`BaseBounds <gemd.entity.bounds.base_bounds.BaseBounds>`
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
        """Get the bounds."""
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        if bounds is None:
            raise ValueError("Bounds are required on AttributeTemplate")
        if not isinstance(bounds, BaseBounds):
            raise TypeError("Bounds must be an instance of BaseBounds: {}".format(bounds))
        self._bounds = bounds

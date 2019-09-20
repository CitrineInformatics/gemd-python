"""Attribute templates."""
from taurus.entity.base_entity import BaseEntity
from taurus.entity.bounds.base_bounds import BaseBounds


class AttributeTemplate(BaseEntity):
    """
    An attribute template, which can be a property, parameter, or condition template.

    Parameters
    ----------
    name: str
        The name of the attribute template.
    bounds: :py:class:`BaseBounds <taurus.entity.bounds.base_bounds.BaseBounds>`
        Bounds circumscribe the values that are valid according to this attribute template.
    description: str, optional
        A long-form description of the attribute template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.

    """

    def __init__(self, name=None, description=None, bounds=None, uids=None, tags=None):
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
    def bounds(self, value):
        if value is None:
            raise ValueError("Bounds are required on AttributeTemplate")
        if not isinstance(value, BaseBounds):
            raise ValueError("Bounds must be an instance of BaseBounds")
        self._bounds = value

    def validate(self, attribute):
        """
        Check that the attribute is consistent with this template.

        This method returns True/False instead of throwing a ValueError.  If the name or value
        of the attribute is not defined, it is not checked (i.e. default True).

        :param attribute: to check the validity of
        :return: True if valid and False if invalid
        """
        if attribute.name != self.name:
            return False

        if attribute.value is not None and not self.bounds.validate(attribute.value):
            return False

        return True

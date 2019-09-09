"""Attribute templates."""
from taurus.entity.base_entity import BaseEntity
from taurus.entity.bounds.base_bounds import BaseBounds


class AttributeTemplate(BaseEntity):
    """
    Class for all attribute templates, which must contain a bounds and scope.

    The bounds implies the type of the template, e.g. RealBounds imply data_type = DataType.REAL.
    """

    skip = ["_data_type"]

    def __init__(self, name=None, description=None, bounds=None, uids=None, tags=None):
        """
        Create an attribute template.

        :param name: of the template and attributes that it describes
        :param description: of the attribute that the template describes
        :param bounds: bounds for data type
        :param uids: from BaseEntity
        :param tags: from BaseEntity
        """
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

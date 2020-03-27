"""For entities that have properties."""
from gemd.entity.attribute.property import Property
from gemd.entity.setters import validate_list


class HasProperties(object):
    """Mixin-trait for entities that include properties."""

    def __init__(self, properties):
        self._properties = None
        self.properties = properties

    @property
    def properties(self):
        """Get a list of the properties."""
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = validate_list(properties, Property)

from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.property import Property
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.setters import validate_list


class PropertyAndConditions(DictSerializable):
    """
    A property and the conditions under which that property was determined.

    This attribute is only relevant for material specs.

    Parameters
    ----------
    property: Property
        A property attribute
    conditions: List[Condition]
        An optional list of conditions associated with this property.

    """

    typ = "property_and_conditions"

    def __init__(self, property=None, conditions=None):
        self._property = None
        self.property = property
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self):
        """Get conditions."""
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        self._conditions = validate_list(conditions, Condition)

    # Horrible hacks to make templates work in the short term
    @property
    def name(self):
        """Get name of attribute (use name of property)."""
        return self.property.name

    @property
    def template(self):
        """Get template of attribute (use template of property)."""
        return self.property.template

    @property
    def origin(self):
        """Get origin of attribute (use origin of property)."""
        return self.property.origin

    @property
    def value(self):
        """Get value of attribute (use value of property)."""
        return self.property.value

    # NOTE: this definition must go last, or else it overrides the property decorator
    @property
    def property(self):
        """Get property."""
        return self._property

    @property.setter
    def property(self, value):
        if isinstance(value, Property):
            self._property = value
        else:
            raise TypeError("property must be a Property")

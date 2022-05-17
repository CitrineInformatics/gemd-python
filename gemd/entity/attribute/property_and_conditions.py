from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.property import Property
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.value.base_value import BaseValue
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list

from typing import Optional, Union, Iterable, List


class PropertyAndConditions(DictSerializable):
    """
    A property and the conditions under which that property was determined.

    This attribute is only relevant for material specs.

    Parameters
    ----------
    property: :class:`Property <gemd.entity.attribute.property.Property>`
        A property attribute
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`]
        An optional list of conditions associated with this property.

    """

    typ = "property_and_conditions"

    def __init__(self,
                 property: Property = None,
                 conditions: Union[Iterable[Condition], Condition] = None):
        self._property = None
        self.property = property
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self) -> List[Condition]:
        """Get conditions."""
        return self._conditions

    @conditions.setter
    def conditions(self, conditions: Iterable[Condition]):
        self._conditions = validate_list(conditions, Condition)

    # Horrible hacks to make templates work in the short term
    @property
    def name(self) -> str:
        """Get name of attribute (use name of property)."""
        return self.property.name

    @property
    def template(self) -> Optional[Union[PropertyTemplate, LinkByUID]]:
        """Get template of attribute (use template of property)."""
        return self.property.template

    @property
    def origin(self) -> str:
        """Get origin of attribute (use origin of property)."""
        return self.property.origin

    @property
    def value(self) -> BaseValue:
        """Get value of attribute (use value of property)."""
        return self.property.value

    # NOTE: this definition must go last, or else it overrides the property decorator
    @property
    def property(self) -> Property:
        """Get property."""
        return self._property

    @property.setter
    def property(self, value: Property):
        if isinstance(value, Property):
            self._property = value
        else:
            raise TypeError("property must be a Property")

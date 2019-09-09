"""Condition class."""
from taurus.entity.attribute.base_attribute import BaseAttribute
from taurus.enumeration import AttributeType


class Condition(BaseAttribute):
    """Condition of a property, process, or measurement."""

    typ = "condition"
    attribute_type = AttributeType.CONDITION

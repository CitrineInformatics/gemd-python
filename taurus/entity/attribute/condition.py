"""Condition class."""
from taurus.entity.attribute.base_attribute import BaseAttribute
from taurus.enumeration import AttributeType


class Condition(BaseAttribute):
    """
    Condition of a property, process, or measurement.

    Conditions are environmental variables (typically measured) that may affect a process
    or measurement: e.g., temperature, pressure.

    """

    typ = "condition"
    attribute_type = AttributeType.CONDITION

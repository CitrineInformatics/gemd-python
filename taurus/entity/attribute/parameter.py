"""Parameter class."""
from taurus.entity.attribute.base_attribute import BaseAttribute
from taurus.enumeration import AttributeType


class Parameter(BaseAttribute):
    """Parameter of a process or measurement."""

    typ = "parameter"
    attribute_type = AttributeType.PARAMETER

"""All possible attributes that an entity can have."""
from taurus.enumeration.base_enumeration import BaseEnumeration


class AttributeType(BaseEnumeration):
    """Enumeration containing all possible attribute types."""

    PROPERTY = "property"
    PARAMETER = "parameter"
    CONDITION = "condition"
    METADATA = "metadata"

"""
Metadata class.

THIS IS CURRENTLY UNUSED.
We might use it in the future, but its not currently part of the spec
"""

from taurus.entity.attribute.base_attribute import BaseAttribute
from taurus.enumeration import AttributeType


class Metadata(BaseAttribute):
    """Ancillary information about a material or process."""

    typ = "metadata"
    attribute_type = AttributeType.METADATA

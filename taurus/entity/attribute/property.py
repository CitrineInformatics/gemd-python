"""Property class."""
from taurus.entity.attribute.base_attribute import BaseAttribute
from taurus.enumeration import AttributeType


class Property(BaseAttribute):
    """
    Property of a material, measured in a MeasurementRun or specified in a MaterialSpec.

    Properties are characteristics of a material that could be measured, e.g. chemical composition,
     density, yield strength.

    """

    typ = "property"
    attribute_type = AttributeType.PROPERTY

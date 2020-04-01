from gemd.entity.attribute.base_attribute import BaseAttribute


class Condition(BaseAttribute):
    """
    Condition of a property, process, or measurement.

    Conditions are environmental variables (typically measured) that may affect a process
    or measurement: e.g., temperature, pressure.

    """

    typ = "condition"

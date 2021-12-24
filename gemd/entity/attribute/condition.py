from gemd.entity.attribute.base_attribute import BaseAttribute
from gemd.entity.template import ConditionTemplate

from typing import Type


class Condition(BaseAttribute):
    """
    Condition of a property, process, or measurement.

    Conditions are environmental variables (typically measured) that may affect a process
    or measurement: e.g., temperature, pressure.

    Parameters
    ----------
    name: str
        Required name of the attribute. Each attribute within an object must have a unique name.
    notes: str
        Optional free-form notes about the attribute.
    value: :class:`BaseValue <gemd.entity.value.base_value.BaseValue>`
        The value of the attribute.
    template: :class:`AttributeTemplate \
    <gemd.entity.template.attribute_template.AttributeTemplate>`
        Attribute template that defines the allowed bounds of this attribute. If a template
        and value are both present then the value must be within the template bounds.
    origin: str
        The origin of the attribute. Must be one of "measured", "predicted", "summary",
        "specified", "computed", or "unknown." Default is "unknown."
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`]
        Links to files associated with the attribute.

    """

    typ = "condition"

    @staticmethod
    def _template_type() -> Type:
        return ConditionTemplate

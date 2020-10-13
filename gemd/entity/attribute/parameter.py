from gemd.entity.attribute.base_attribute import BaseAttribute
from gemd.entity.template import ParameterTemplate

from typing import Type


class Parameter(BaseAttribute):
    """
    Parameter of a process or measurement.

    Parameters are the non-environmental variables (typically specified and controlled) that may
    affect a process or measurement: e.g. oven dial temperature for a kiln firing, magnification
    for a measurement taken with an electron microscope.

    """

    typ = "parameter"

    @staticmethod
    def _template_type() -> Type:
        return ParameterTemplate

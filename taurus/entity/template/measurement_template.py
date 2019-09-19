"""A measurement template."""
from taurus.entity.object import MeasurementRun
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.has_condition_templates import HasConditionTemplates
from taurus.entity.template.has_parameter_templates import HasParameterTemplates
from taurus.entity.template.has_property_templates import HasPropertyTemplates


class MeasurementTemplate(BaseTemplate,
                          HasPropertyTemplates, HasConditionTemplates, HasParameterTemplates):
    """Template for measurements, containing property, parameter, and condition templates."""

    typ = "measurement_template"

    def __init__(self,
                 name=None, description=None,
                 properties=None, conditions=None, parameters=None,
                 uids=None, tags=None):
        BaseTemplate.__init__(self, name, description, uids, tags)
        HasPropertyTemplates.__init__(self, properties)
        HasConditionTemplates.__init__(self, conditions)
        HasParameterTemplates.__init__(self, parameters)

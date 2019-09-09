"""For entities that have a parameter template."""
from taurus.entity.setters import validate_list
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.parameter_template import ParameterTemplate


class HasParameterTemplates(object):
    """Mixin-trait for entities that include parameter templates."""

    def __init__(self, parameters):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self):
        """Get the list of parameter templates."""
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        lst = validate_list(parameters, (ParameterTemplate, list, tuple))

        # make sure attribute can be a Parameter
        # TODO: list.map(_.validate_scope(AttributeType.PARAMETER)) all true

        self._parameters = list(map(BaseTemplate._homogenize_ranges, lst))

    def validate_parameters(self, obj):
        """Validate an object's parameters against its templates."""
        BaseTemplate._validate_attributes(self, obj, "parameters")

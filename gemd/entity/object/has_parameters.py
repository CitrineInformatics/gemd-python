"""For entities that have parameters."""
from gemd.entity.template.has_parameter_templates import HasParameterTemplates
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.setters import validate_list
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger


class HasParameters(object):
    """Mixin-trait for entities that include parameters.

    Parameters
    ----------
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`]
        A list of parameters associated with this entity.

    """

    def __init__(self, parameters):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self):
        """Get the list of parameters."""
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        def _template_check(x: Parameter) -> Parameter:
            # if Has_Templates hasn't been called yet, it won't have a _template attribute
            template = getattr(self, "template", None)
            level = get_validation_level()
            accept = level == WarningLevel.IGNORE \
                or not isinstance(template, HasParameterTemplates) \
                or self.template.validate_parameter(x)

            if not accept:
                message = f"Value {x.value} is inconsistent with template {template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)
            return x

        self._parameters = validate_list(parameters, Parameter, trigger=_template_check)

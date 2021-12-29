"""For entities that have conditions."""
from gemd.entity.template.has_condition_templates import HasConditionTemplates
from gemd.entity.attribute.condition import Condition
from gemd.entity.setters import validate_list
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger


class HasConditions(object):
    """Mixin-trait for entities that include conditions.

    Parameters
    ----------
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`]
        A list of conditions associated with this entity.

    """

    def __init__(self, conditions):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self):
        """Get a list of the conditions."""
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        def _template_check(x: Condition) -> Condition:
            # if Has_Templates hasn't been called yet, it won't have a _template attribute
            template = getattr(self, "template", None)
            level = get_validation_level()
            accept = level == WarningLevel.IGNORE \
                or not isinstance(template, HasConditionTemplates) \
                or self.template.validate_condition(x)

            if not accept:
                message = f"Value {x.value} is inconsistent with template {template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)
            return x

        self._conditions = validate_list(conditions, Condition, trigger=_template_check)

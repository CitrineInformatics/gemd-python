"""For entities that have conditions."""
from gemd.entity.attribute.condition import Condition
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.setters import validate_list
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger

from typing import Iterable, List, Set


class HasConditions(object):
    """Mixin-trait for entities that include conditions.

    Parameters
    ----------
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`]
        A list of conditions associated with this entity.

    """

    def __init__(self, conditions: Iterable[Condition]):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self) -> List[Condition]:
        """Get a list of the conditions."""
        return self._conditions

    @conditions.setter
    def conditions(self, conditions: Iterable[Condition]):
        """Set the list of conditions."""
        def _template_check(x: Condition) -> Condition:
            # if Has_Templates hasn't been called yet, it won't have a _template attribute
            template = getattr(self, "template", None)
            level = get_validation_level()
            accept = level == WarningLevel.IGNORE or template is None \
                or self.template.validate_condition(x)

            if not accept:
                message = f"Value {x.value} is inconsistent with template {template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)
            return x

        self._conditions = validate_list(conditions, Condition, trigger=_template_check)

    def all_dependencies(self) -> Set[ConditionTemplate]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {cond.template for cond in self.conditions if cond.template is not None}

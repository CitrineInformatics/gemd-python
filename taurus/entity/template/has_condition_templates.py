"""For entities that have a condition template."""
from taurus.entity.setters import validate_list
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.condition_template import ConditionTemplate


class HasConditionTemplates(object):
    """Mixin-trait for entities that include condition template."""

    def __init__(self, conditions):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self):
        """Get the list of condition templates."""
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        lst = validate_list(conditions, (ConditionTemplate, list, tuple))

        # make sure attribute can be a Condition
        # TODO: list.map(_.validate_scope(AttributeType.CONDITION)) all true

        self._conditions = list(map(BaseTemplate._homogenize_ranges, lst))

    def validate_conditions(self, obj):
        """Validate an object's conditions against its template."""
        BaseTemplate._validate_attributes(self, obj, "conditions")

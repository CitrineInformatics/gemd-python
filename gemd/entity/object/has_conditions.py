"""For entities that have conditions."""
from gemd.entity.attribute.condition import Condition
from gemd.entity.setters import validate_list


class HasConditions(object):
    """Mixin-trait for entities that include conditions."""

    def __init__(self, conditions):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self):
        """Get a list of the conditions."""
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        self._conditions = validate_list(conditions, Condition)

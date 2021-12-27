"""For entities that have conditions."""
from gemd.entity.attribute.condition import Condition
from gemd.entity.setters import validate_list


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
        """Set the list of conditions."""
        self._conditions = validate_list(conditions, Condition)

    def all_dependencies(self):
        """Return a set of all immediate dependencies (no recursion)."""
        return {cond.template for cond in self.conditions if cond.template is not None}

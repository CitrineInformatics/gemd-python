"""For entities that have conditions."""
from gemd.entity.attribute.condition import Condition
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.setters import validate_list

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
        self._conditions = validate_list(conditions, Condition)

    def all_dependencies(self) -> Set[ConditionTemplate]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {cond.template for cond in self.conditions if cond.template is not None}

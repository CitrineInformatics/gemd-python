"""For entities that have a condition template."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.bounds.base_bounds import BaseBounds

from typing import TypeVar, Optional, Union, Iterable, List, Tuple, Set

__all__ = ["HasConditionTemplates"]
BaseEntityType = TypeVar("BaseEntityType", bound="BaseEntity")  # noqa: F821
ConditionType = TypeVar("ConditionType", bound="Condition")  # noqa: F821


class HasConditionTemplates(HasDependencies):
    """
    Mixin-trait for entities that include condition templates.

    Parameters
    ----------
    conditions: List[(~gemd.entity.template.condition_template.ConditionTemplate, BaseBounds)]
        A list of tuples containing this entity's condition templates as well
        as any restrictions on those templates' bounds.

    """

    def __init__(self, conditions: Iterable[Union[Union[ConditionTemplate, LinkByUID],
                                                  Tuple[Union[ConditionTemplate, LinkByUID],
                                                        Optional[BaseBounds]]]]):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self) -> List[Union[ConditionTemplate, LinkByUID]]:
        """
        Get the list of condition template/bounds tuples.

        Returns
        -------
        List[(~gemd.entity.template.condition_template.ConditionTemplate, BaseBounds)]
            List of this entity's condition template/bounds pairs

        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions: Iterable[Union[Union[ConditionTemplate, LinkByUID],
                                                    Tuple[Union[ConditionTemplate, LinkByUID],
                                                          Optional[BaseBounds]]]]):
        """
        Set the list of condition templates.

        Parameters
        ----------
        conditions: List[(~gemd.entity.template.condition_template.ConditionTemplate, BaseBounds)]
            A list of tuples containing this entity's condition templates as well
            as any restrictions on those templates' bounds.

        Returns
        -------
        List[(~gemd.entity.template.condition_template.ConditionTemplate, BaseBounds)]
            List of this entity's condition template/bounds pairs

        """
        if isinstance(conditions, Iterable):
            if any(isinstance(x, BaseBounds) for x in conditions):
                conditions = [conditions]  # It's a template/bounds tuple (probably)
        self._conditions = validate_list(conditions,
                                         (ConditionTemplate, LinkByUID, list, tuple),
                                         trigger=BaseTemplate._homogenize_ranges
                                         )

    def validate_condition(self, condition: ConditionType) -> bool:
        """Check if the condition is consistent w/ this template."""
        if condition.template is not None:
            attr, bnd = next((x for x in self.conditions if condition.template == x[0]),
                             (None, None))
        else:
            attr, bnd = next((x for x in self.conditions if condition.name == x[0].name),
                             (None, None))

        if bnd is not None:
            return bnd.contains(condition.value)
        elif attr is not None and isinstance(attr, ConditionTemplate):
            return attr.bounds.contains(condition.value)
        else:
            return True  # Nothing to check against

    def _local_dependencies(self) -> Set[Union[BaseEntityType, LinkByUID]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {attr[0] for attr in self.conditions}

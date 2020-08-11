"""For entities that have a condition template."""
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.bounds.base_bounds import BaseBounds
from typing import Iterable


class HasConditionTemplates(object):
    """
    Mixin-trait for entities that include condition templates.

    Parameters
    ----------
    conditions: List[(ConditionTemplate, BaseBounds)]
        A list of tuples containing this entity's condition templates as well
        as any restrictions on those templates' bounds.

    """

    def __init__(self, conditions):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self):
        """
        Get the list of condition template/bounds tuples.

        Returns
        -------
        List[(ConditionTemplate, bounds)]
            List of this entity's condition template/bounds pairs

        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """
        Set the list of condition templates.

        Parameters
        ----------
        conditions: List[(ConditionTemplate, bounds)]
            A list of tuples containing this entity's condition templates as well
            as any restrictions on those templates' bounds.

        Returns
        -------
        List[(ConditionTemplate, bounds)]
            List of this entity's condition template/bounds pairs

        """
        if isinstance(conditions, Iterable):
            if any(isinstance(x, BaseBounds) for x in conditions):
                conditions = [conditions]  # It's a template/bounds tuple (probably)
        self._conditions = validate_list(conditions,
                                         (ConditionTemplate, LinkByUID, list, tuple),
                                         trigger=BaseTemplate._homogenize_ranges
                                         )

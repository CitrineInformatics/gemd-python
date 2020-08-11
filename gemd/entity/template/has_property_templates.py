"""For entities that have a property template."""
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.bounds.base_bounds import BaseBounds
from typing import Iterable


class HasPropertyTemplates(object):
    """
    Mixin-trait for entities that include property templates.

    Parameters
    ----------
    properties: List[(PropertyTemplate, BaseBounds)]
        A list of tuples containing this entity's property templates as well
        as any restrictions on those templates' bounds.

    """

    def __init__(self, properties):
        self._properties = None
        self.properties = properties

    @property
    def properties(self):
        """
        Get the list of property template/bounds tuples.

        Returns
        -------
        List[(PropertyTemplate, bounds)]
            List of this entity's property template/bounds pairs

        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Set the list of parameter templates.

        Parameters
        ----------
        properties: List[(PropertyTemplate, bounds)]
            A list of tuples containing this entity's property templates as well
            as any restrictions on those templates' bounds.

        Returns
        -------
        List[(PropertyTemplate, bounds)]
            List of this entity's property template/bounds pairs

        """
        if isinstance(properties, Iterable):
            if any(isinstance(x, BaseBounds) for x in properties):
                properties = [properties]  # It's a template/bounds tuple (probably)
        self._properties = validate_list(properties,
                                         (PropertyTemplate, LinkByUID, list, tuple),
                                         trigger=BaseTemplate._homogenize_ranges
                                         )

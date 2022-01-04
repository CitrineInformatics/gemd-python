"""For entities that have a property template."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.bounds.base_bounds import BaseBounds

from typing import Optional, Union, Iterable, List, Set, Tuple


class HasPropertyTemplates(HasDependencies):
    """
    Mixin-trait for entities that include property templates.

    Parameters
    ----------
    properties: List[(PropertyTemplate, BaseBounds)]
        A list of tuples containing this entity's property templates as well
        as any restrictions on those templates' bounds.

    """

    def __init__(self, properties: Iterable[Union[Union[PropertyTemplate, LinkByUID],
                                                  Tuple[Union[PropertyTemplate, LinkByUID],
                                                        Optional[BaseBounds]]]]):
        self._properties = None
        self.properties = properties

    @property
    def properties(self) -> List[Tuple[Union[PropertyTemplate, LinkByUID],
                                       Optional[BaseBounds]]]:
        """
        Get the list of property template/bounds tuples.

        Returns
        -------
        List[(PropertyTemplate, bounds)]
            List of this entity's property template/bounds pairs

        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Union[Union[PropertyTemplate, LinkByUID],
                                                    Tuple[Union[PropertyTemplate, LinkByUID],
                                                          Optional[BaseBounds]]]]):
        """
        Set the list of parameter templates.

        Parameters
        ----------
        properties: List[(PropertyTemplate, bounds)]
            A list of tuples containing this entity's property templates as well
            as any restrictions on those templates' bounds.

        """
        if isinstance(properties, Iterable):
            if any(isinstance(x, BaseBounds) for x in properties):
                properties = [properties]  # It's a template/bounds tuple (probably)
        self._properties = validate_list(properties,
                                         (PropertyTemplate, LinkByUID, list, tuple),
                                         trigger=BaseTemplate._homogenize_ranges
                                         )

    def validate_property(self, prop: Union["Property", "PropertyAndConditions"]) -> bool:
        """Check if the property is consistent w/ this template."""
        from gemd.entity.attribute import PropertyAndConditions
        if isinstance(prop, PropertyAndConditions):
            prop = prop.property

        if prop.template is not None:
            attr, bnd = next((x for x in self.properties if prop.template == x[0]),
                             (None, None))
        else:
            attr, bnd = next((x for x in self.properties if prop.name == x[0].name),
                             (None, None))

        if bnd is not None:
            return bnd.contains(prop.value)
        elif attr is not None and isinstance(attr, PropertyTemplate):
            return attr.bounds.contains(prop.value)
        else:
            return True  # Nothing to check against

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {attr[0] for attr in self.properties}

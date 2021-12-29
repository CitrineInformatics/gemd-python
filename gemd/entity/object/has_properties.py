"""For entities that have properties."""
from gemd.entity.attribute.property import Property
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.setters import validate_list
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger

from typing import Iterable, List, Set


class HasProperties(object):
    """Mixin-trait for entities that include properties.

    Parameters
    ----------
    properties: List[:class:`Property <gemd.entity.attribute.property.Property>`]
        A list of properties associated with this entity

    """

    def __init__(self, properties: Iterable[Property]):
        self._properties = None
        self.properties = properties

    @property
    def properties(self) -> List[Property]:
        """Get a list of the properties."""
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]):
        """Set the list of properties."""
        def _template_check(x: Property) -> Property:
            # if Has_Templates hasn't been called yet, it won't have a _template attribute
            template = getattr(self, "template", None)
            level = get_validation_level()
            accept = level == WarningLevel.IGNORE or template is None \
                or self.template.validate_property(x)

            if not accept:
                message = f"Value {x.value} is inconsistent with template {template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)
            return x

        self._properties = validate_list(properties, Property, trigger=_template_check)

    def all_dependencies(self) -> Set[PropertyTemplate]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {prop.template for prop in self.properties if prop.template is not None}

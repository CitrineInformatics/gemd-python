"""For entities that have properties."""
from gemd.entity.template.has_property_templates import HasPropertyTemplates
from gemd.entity.attribute.property import Property
from gemd.entity.setters import validate_list
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger


class HasProperties(object):
    """Mixin-trait for entities that include properties.

    Parameters
    ----------
    properties: List[:class:`Property <gemd.entity.attribute.property.Property>`]
        A list of properties associated with this entity

    """

    def __init__(self, properties):
        self._properties = None
        self.properties = properties

    @property
    def properties(self):
        """Get a list of the properties."""
        return self._properties

    @properties.setter
    def properties(self, properties):
        def _template_check(x: Property) -> Property:
            # if Has_Templates hasn't been called yet, it won't have a _template attribute
            template = getattr(self, "template", None)
            level = get_validation_level()
            accept = level == WarningLevel.IGNORE \
                or not isinstance(template, HasPropertyTemplates) \
                or self.template.validate_property(x)

            if not accept:
                message = f"Value {x.value} is inconsistent with template {template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)
            return x

        self._properties = validate_list(properties, Property, trigger=_template_check)

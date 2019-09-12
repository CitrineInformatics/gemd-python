"""Base template."""
from taurus.entity.base_entity import BaseEntity
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.template.attribute_template import AttributeTemplate


class BaseTemplate(BaseEntity):
    """Base class for all templates."""

    def __init__(self, name=None, description=None, uids=None, tags=None):
        BaseEntity.__init__(self, uids, tags)
        self.name = name
        self.description = description

    def validate(self, obj):
        """Validate an object against the template."""
        raise NotImplementedError(
            "Subclass of BaseTemplate didn't implement validate: {}".format(type(self)))

    @staticmethod
    def _homogenize_ranges(template_or_tuple):
        """Take either a template or pair and turn it into a (template, bounds) pair."""
        # if given a template, pull out its bounds
        if isinstance(template_or_tuple, AttributeTemplate):
            return [template_or_tuple, template_or_tuple.bounds]
        # if given a (template, bounds) pair,
        # check that the bounds is consistent with that of the template
        elif isinstance(template_or_tuple, (tuple, list)):
            first, second = template_or_tuple
            if isinstance(first, LinkByUID) and isinstance(second, BaseBounds):
                return [first, second]
            if isinstance(first, AttributeTemplate) and isinstance(second, BaseBounds):
                if first.bounds.contains(second):
                    return [first, second]
                else:
                    raise ValueError("Range and template are inconsistent")
        raise ValueError("Expected a template or (template, bounds) tuple")

    @staticmethod
    def _validate_attributes(template, obj, attr_name):
        """Validate a specific attribute in an object against its template."""
        # Skip validation if the object doesn't contain the attribute,
        # e.g. MaterialRun doesn't contain properties
        if not hasattr(obj, attr_name):
            return

        # check each contained (template, bounds)
        for (attr_template, bounds) in getattr(template, attr_name):

            # find any attributes that match the name
            name = getattr(attr_template, 'name', None)
            for attribute in filter(lambda x: x.name == name, getattr(obj, attr_name)):
                # make sure the value is within the accepted range (the bounds)
                if not bounds.validate(attribute.value):
                    raise RuntimeWarning(
                        "Template and object do not match: attribute '{attr_name}' has value "
                        "{val}, which is invalid against bounds {bounds}".format(
                            attr_name=attribute.name, val=attribute.value, bounds=bounds)
                    )

                # if the attribute doesn't have a template, assign this template to it
                if attribute.template is None:
                    attribute.template = attr_template
                # if it does have a template and its not a LinkByUID, make sure its the right one
                elif attribute.template != attr_template \
                        and isinstance(attribute.template, AttributeTemplate) \
                        and isinstance(attr_template, AttributeTemplate):
                    raise ValueError(
                        "Template and object templates don't match for all {}".format(attr_name))

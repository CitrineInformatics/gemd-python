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

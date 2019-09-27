"""Base template."""
from taurus.entity.base_entity import BaseEntity
from taurus.entity.bounds.base_bounds import BaseBounds
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.template.attribute_template import AttributeTemplate


class BaseTemplate(BaseEntity):
    """
    Base class for all object templates.

    Parameters
    ----------
    name: str, optional
        The name of the object template.
    description: str, optional
        Long-form description of the object template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.

    """

    def __init__(self, name=None, description=None, uids=None, tags=None):
        BaseEntity.__init__(self, uids, tags)
        self.name = name
        self.description = description

    @staticmethod
    def _homogenize_ranges(template_or_tuple):
        """
        Take either a template or pair and turn it into a (template, bounds) pair.

        If no bounds are provided, use the attribute template's default bounds.

        Parameters
        ----------
        template_or_tuple: AttributeTemplate OR a list or
        tuple [AttributeTemplate or LinkByUID, BaseBounds]
           An attribute template, optionally with another Bounds object that is more
           restrictive than the attribute template's default bounds.

        Returns
        -------
        List[AttributeTemplate or LinkByUID, BaseBounds]
            The attribute template and bounds that should be applied the the attribute
            when used in the context of **this** object.

        """
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
        raise TypeError("Expected a template or (template, bounds) tuple")  # pragma: no cover

"""Base template."""
from gemd.entity.base_entity import BaseEntity
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.template.attribute_template import AttributeTemplate


class BaseTemplate(BaseEntity):
    """
    Base class for all object templates.

    Parameters
    ----------
    name: str, required
        The name of the object template.
    description: str, optional
        Long-form description of the object template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.

    """

    def __init__(self, name, *, description=None, uids=None, tags=None):
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
        # if given a template only, use None to represent passthrough bounds
        if isinstance(template_or_tuple, (AttributeTemplate, LinkByUID)):
            return [template_or_tuple, None]
        # if given a (template, bounds) pair,
        # check that the bounds is consistent with that of the template
        elif isinstance(template_or_tuple, (tuple, list)):
            first, second = template_or_tuple
            if isinstance(first, (LinkByUID, AttributeTemplate)) and \
                    (isinstance(second, BaseBounds) or second is None):
                if isinstance(first, AttributeTemplate) and isinstance(second, BaseBounds):
                    if not first.bounds.contains(second):
                        raise ValueError("Range and template are inconsistent")
                return [first, second]
        raise TypeError("Expected a template or (template, bounds) tuple")  # pragma: no cover

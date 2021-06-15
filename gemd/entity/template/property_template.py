from gemd.entity.template.attribute_template import AttributeTemplate


class PropertyTemplate(AttributeTemplate):
    """A template for the property attribute.

    Parameters
    ----------
    name: str, required
        The name of the property template.
    bounds: :py:class:`BaseBounds <gemd.entity.bounds.base_bounds.BaseBounds>`
        Bounds circumscribe the values that are valid according to this property template.
    description: str, optional
        A long-form description of the attribute template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.

    """

    typ = "property_template"

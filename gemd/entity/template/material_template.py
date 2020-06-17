"""A material template."""
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.has_property_templates import HasPropertyTemplates


class MaterialTemplate(BaseTemplate, HasPropertyTemplates):
    """
    A material template.

    Material templates are collections of property templates that constrain the values of
    a material's property attributes, and provide a common structure for describing similar
    materials.

    Parameters
    ----------
    name: str, required
        The name of the material template.
    description: str, optional
        Long-form description of the material template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    properties: List[:class:`PropertyTemplate \
    <gemd.entity.template.property_template.PropertyTemplate>`] or \
    List[:class:`PropertyTemplate <gemd.entity.template.property_template.PropertyTemplate>`,\
     :py:class:`BaseBounds <gemd.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated properties. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this property.

    """

    typ = "material_template"

    def __init__(self, name, *, description=None,
                 properties=None,
                 uids=None, tags=None):
        BaseTemplate.__init__(self, name=name, description=description,
                              uids=uids, tags=tags
                              )
        HasPropertyTemplates.__init__(self, properties)

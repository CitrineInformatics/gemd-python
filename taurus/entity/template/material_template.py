"""A material template."""
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.has_property_templates import HasPropertyTemplates
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions


class MaterialTemplate(BaseTemplate, HasPropertyTemplates):
    """
    A material template.

    Material templates are collections of property templates that constrain the values of
    a material's property attributes, and provide a common structure for describing similar
    materials.

    Parameters
    ----------
    name: str, optional
        The name of the material template.
    description: str, optional
        Long-form description of the material template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    properties: List[:class:`PropertyTemplate \
    <taurus.entity.template.property_template.PropertyTemplate>`] or \
    List[:class:`PropertyTemplate <taurus.entity.template.property_template.PropertyTemplate>`,\
     :py:class:`BaseBounds <taurus.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated properties. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this property.

    """

    typ = "material_template"

    def __init__(self, name=None, description=None, properties=None, uids=None, tags=None):
        BaseTemplate.__init__(self, name, description, uids, tags)
        HasPropertyTemplates.__init__(self, properties)

    def __call__(
        self,
        name=None,
        template=None,
        properties=None,
        process=None,
        uids=None,
        tags=None,
        notes=None,
        file_links=None,
    ):
        """Produces a material spec that is linked to this material template."""

        if not name:  # inherit name from the template by default
            name = self.name
        if not template:  # link the material spec to this template by default
            template = self
        if not properties:  # inherit the properties from the template (empty values)
            properties = [
                PropertyAndConditions(property=prop_template())
                for prop_template, bounds in self.properties
            ]

        return MaterialSpec(
            name=name,
            template=template,
            properties=properties,
            process=process,
            uids=uids,
            tags=tags,
            notes=notes,
            file_links=file_links,
        )

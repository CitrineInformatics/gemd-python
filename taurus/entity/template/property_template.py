from taurus.entity.template.attribute_template import AttributeTemplate
from taurus.entity.attribute.property import Property


class PropertyTemplate(AttributeTemplate):
    """A template for the property attribute."""

    typ = "property_template"

    def __call__(
        self, name=None, template=None, origin="unknown", value=None, notes=None, file_links=None
    ):
        """Produces a property that is linked to this template."""

        if not name:  # inherit name from the template by default
            name = self.name

        if not template:  # link the property to this template by default
            template = self

        return Property(
            name=name,
            template=template,
            origin=origin,
            value=value,
            notes=notes,
            file_links=file_links,
        )

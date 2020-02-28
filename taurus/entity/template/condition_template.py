from taurus.entity.template.attribute_template import AttributeTemplate
from taurus.entity.attribute.condition import Condition


class ConditionTemplate(AttributeTemplate):
    """A template for a condition attribute."""

    typ = "condition_template"

    def __call__(
        self, name=None, template=None, origin="unknown", value=None, notes=None, file_links=None
    ):
        """Produces a condition that is linked to this condition template."""

        if not name:  # inherit name from the template by default
            name = self.name

        if not template:  # link the condition to this template by default
            template = self

        return Condition(
            name=name,
            template=template,
            origin=origin,
            value=value,
            notes=notes,
            file_links=file_links,
        )

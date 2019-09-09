"""For entities that have templates."""
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.link_by_uid import LinkByUID


class HasTemplate(object):
    """Mix-in trait for objects that can be assigned templates."""

    def __init__(self, template=None):
        self._template = None
        self.template = template

    @property
    def template(self):
        """Get the template."""
        return self._template

    @template.setter
    def template(self, template):
        if template is None:
            self._template = None
        elif isinstance(template, BaseTemplate):
            # run the template validation when the template is assigned
            template.validate(self)
            self._template = template
        elif isinstance(template, LinkByUID):
            # LinkByUID cannot be validated, but is still assigned
            self._template = template
        else:
            raise ValueError("Template must be a template")

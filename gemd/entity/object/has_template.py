"""For entities that have templates."""
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.link_by_uid import LinkByUID


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
        elif isinstance(template, (BaseTemplate, LinkByUID)):
            self._template = template
        else:
            raise TypeError("Template must be a template or LinkByUID: {}".format(template))

"""Base class for all attributes."""
from taurus.entity.dict_serializable import DictSerializable
from taurus.entity.template.attribute_template import AttributeTemplate
from taurus.entity.value.base_value import BaseValue
from taurus.enumeration import Origin
from taurus.entity.setters import validate_list
from taurus.entity.file_link import FileLink
from taurus.entity.link_by_uid import LinkByUID


class BaseAttribute(DictSerializable):
    """Base class for attributes, which include Property, Parameter, Condition, and Metadata."""

    attribute_type = None

    def __init__(self, name=None, template=None, origin="unknown", value=None, notes=None,
                 file_links=None):
        if name is None:
            raise ValueError("Attributes must be named")
        self.name = name
        self.notes = notes

        self._value = None
        self._template = None
        self._origin = None
        self._file_links = None,

        self.value = value
        self.template = template
        self.origin = origin
        self.file_links = file_links

    @property
    def value(self):
        """Get value."""
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = None
        elif isinstance(value, (BaseValue, str, bool)):
            self._value = value
        else:
            raise ValueError("value must be a BaseValue, string or bool")

    @property
    def template(self):
        """Get template."""
        return self._template

    @template.setter
    def template(self, template):
        if template is None:
            self._template = None
        elif isinstance(template, (LinkByUID, AttributeTemplate)):
            self._template = template
        else:
            raise ValueError("template must be a BaseAttributeTemplate or LinkByUID")

    @property
    def origin(self):
        """Get origin."""
        return self._origin

    @origin.setter
    def origin(self, origin):
        if origin is None:
            raise ValueError("origin must be specified (but may be `unknown`)")
        self._origin = Origin.get_value(origin)

    @property
    def file_links(self):
        """Get file links."""
        return self._file_links

    @file_links.setter
    def file_links(self, file_links):
        self._file_links = validate_list(file_links, FileLink)

from taurus.entity.dict_serializable import DictSerializable
from taurus.entity.template.attribute_template import AttributeTemplate
from taurus.entity.value.base_value import BaseValue
from taurus.enumeration import Origin
from taurus.entity.setters import validate_list
from taurus.entity.file_link import FileLink
from taurus.entity.link_by_uid import LinkByUID


class BaseAttribute(DictSerializable):
    """
    Base class for all attributes, which include property, condition, parameter, and metadata.

    Parameters
    ----------
    name: str
        Required name of the attribute. Each attribute within an object must have a unique name.
    notes: str
        Optional free-form notes about the attribute.
    value: :py:class:`BaseValue <taurus.entity.value.base_value.BaseValue>`
        The value of the attribute.
    template: :class:`AttributeTemplate \
    <taurus.entity.template.attribute_template.AttributeTemplate>`
        Attribute template that defines the allowed bounds of this attribute. If a template
        and value are both present then the value must be within the template bounds.
    origin: str
        The origin of the attribute. Must be one of "measured", "predicted", "summary",
        "specified", "computed", or "unknown." Default is "unknown."
    file_links: List[FileLink]
        Links to files associated with the attribute.

    """

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

        # TODO: Make template required (need to fix a bunch of unit tests)
        #  if self.template is None:
        #    raise ValueError("Template is required")

    @property
    def value(self):
        """Get value."""
        return self._value

    @value.setter
    def value(self, value):
        if self.template and value and not self.template.bounds.validate(value):
            raise ValueError("the value is inconsistent with the template")

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
        elif isinstance(template, LinkByUID):
            self._template = template
        elif isinstance(template, AttributeTemplate):
            if not template.validate(self):
                raise ValueError("Template is incompatible with attr {}".format(self.name))
            if self.value and not template.bounds.validate(self.value):
                raise ValueError("the template is inconsistent with the value")
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

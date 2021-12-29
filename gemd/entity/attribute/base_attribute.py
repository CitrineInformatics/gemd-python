from gemd.entity.dict_serializable import DictSerializable, logger
from gemd.entity.template.attribute_template import AttributeTemplate
from gemd.entity.value.base_value import BaseValue
from gemd.enumeration import Origin
from gemd.entity.setters import validate_list
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.bounds_validation import get_validation_level, WarningLevel

from typing import Optional, Union, Iterable, List, Type
from abc import abstractmethod


class BaseAttribute(DictSerializable):
    """
    Base class for all attributes, which include property, condition, parameter, and metadata.

    Parameters
    ----------
    name: str
        Required name of the attribute. Each attribute within an object must have a unique name.
    notes: str
        Optional free-form notes about the attribute.
    value: :py:class:`BaseValue <gemd.entity.value.base_value.BaseValue>`
        The value of the attribute.
    template: :class:`AttributeTemplate \
    <gemd.entity.template.attribute_template.AttributeTemplate>`
        Attribute template that defines the allowed bounds of this attribute. If a template
        and value are both present then the value must be within the template bounds.
    origin: str
        The origin of the attribute. Must be one of "measured", "predicted", "summary",
        "specified", "computed", or "unknown." Default is "unknown."
    file_links: List[FileLink]
        Links to files associated with the attribute.

    """

    def __init__(self,
                 name: str,
                 *,
                 template: Union[AttributeTemplate, LinkByUID, None] = None,
                 origin: Union[Origin, str] = Origin.UNKNOWN,
                 value: BaseValue = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
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

    @staticmethod
    def _check(template: AttributeTemplate, value: BaseValue):
        level = get_validation_level()
        accept = level == WarningLevel.IGNORE or template.bounds.contains(value)
        if not accept:
            message = f"template.bounds {template.bounds} does not contain value {value}"
            if level == WarningLevel.WARNING:
                logger.warning(message)
            else:
                raise ValueError(message)

    @property
    def value(self) -> BaseValue:
        """Get value."""
        return self._value

    @value.setter
    def value(self, value: BaseValue):
        if value is None:
            self._value = None
        elif isinstance(value, BaseValue):
            if self.template is not None:
                self._check(self.template, value)
            self._value = value
        else:
            raise TypeError(f"value must be a BaseValue: {value}")

    @property
    def template(self) -> Optional[Union[AttributeTemplate, LinkByUID]]:
        """Get template."""
        return self._template

    @template.setter
    def template(self, template: Optional[Union[AttributeTemplate, LinkByUID]]):
        if template is None:
            self._template = None
        elif isinstance(template, (self._template_type(), LinkByUID)):
            if self.value is not None and isinstance(template, AttributeTemplate):
                self._check(template, self.value)
            self._template = template
        else:
            raise TypeError("template must be a BaseAttributeTemplate or "
                            "LinkByUID: {}".format(template))

    @staticmethod
    @abstractmethod
    def _template_type() -> Type:
        """Get the expected type of template for this object (property of child)."""

    @property
    def origin(self) -> str:
        """Get origin."""
        return self._origin

    @origin.setter
    def origin(self, origin: Union[Origin, str]):
        if origin is None:
            raise ValueError("origin must be specified (but may be `unknown`)")
        self._origin = Origin.get_value(origin)

    @property
    def file_links(self) -> List[FileLink]:
        """Get file links."""
        return self._file_links

    @file_links.setter
    def file_links(self, file_links: Optional[Union[Iterable[FileLink], FileLink]]):
        self._file_links = validate_list(file_links, FileLink)

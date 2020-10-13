"""For entities that have specs."""
from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.link_by_uid import LinkByUID

from typing import Union, Optional, Type
from abc import abstractmethod


class HasSpec(object):
    """Mix-in trait for objects that can be assigned specs."""

    def __init__(self, spec: Union[BaseObject, LinkByUID, None] = None):
        self._spec = None
        self.spec = spec

    @property
    def spec(self) -> Union[BaseObject, LinkByUID, None]:
        """Get the spec."""
        return self._spec

    @spec.setter
    def spec(self, spec: Union[BaseObject, LinkByUID, None]):
        """Set the spec."""
        if spec is None:
            self._spec = None
        elif isinstance(spec, (self._spec_type(), LinkByUID)):
            self._spec = spec
        else:
            raise TypeError("spec must be a spec or LinkByUID: {}".format(spec))

    @staticmethod
    @abstractmethod
    def _spec_type() -> Type:
        """Get the expected type of spec for this object (property of child)."""
        pass

    @property
    def template(self) -> Optional[BaseTemplate]:
        """Get the template of the spec, if applicable."""
        if isinstance(self.spec, HasTemplate):
            return self.spec.template
        else:
            return None

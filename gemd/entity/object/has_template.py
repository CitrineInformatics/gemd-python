"""For entities that have templates."""
from gemd.entity.base_entity import BaseEntity
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.template.base_template import BaseTemplate

from abc import abstractmethod
from typing import Optional, Union, Set, Type

__all__ = ["HasTemplate"]


class HasTemplate(HasDependencies):
    """Mix-in trait for objects that can be assigned templates."""

    def __init__(self, template: Optional[Union[BaseTemplate, LinkByUID]] = None):
        self._template = None
        self.template = template

    @staticmethod
    @abstractmethod
    def _template_type() -> Type:
        """Child must report implementation details."""

    @property
    def template(self) -> Optional[Union[BaseTemplate, LinkByUID]]:
        """A template that defines the allowed values."""
        return self._template

    @template.setter
    def template(self, template: Optional[Union[BaseTemplate, LinkByUID]]):
        """Set the template."""
        if template is None:
            self._template = None
        elif isinstance(template, (self._template_type(), LinkByUID)):
            self._template = template
        else:
            raise TypeError(f"Template must be a {self._template_type()} or LinkByUID, "
                            f"not {type(template)}")

    def _local_dependencies(self) -> Set[Union[BaseEntity, LinkByUID]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.template} if self.template is not None else set()

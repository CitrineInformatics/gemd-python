"""For entities that have templates."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.link_by_uid import LinkByUID

from abc import abstractmethod
from typing import Optional, Union, Set, Type


class HasTemplate(HasDependencies):
    """Mix-in trait for objects that can be assigned templates.

    Parameters
    ----------
    template: :class:`BaseTemplate <gemd.entity.template.base_template.BaseTemplate>`
        A template that defines the allowed values.

    """

    def __init__(self, template: Optional[Union[BaseTemplate, LinkByUID]] = None):
        self._template = None
        self.template = template

    @staticmethod
    @abstractmethod
    def _template_type() -> Type:
        """Child must report implementation details."""

    @property
    def template(self) -> Optional[Union[BaseTemplate, LinkByUID]]:
        """Get the template."""
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

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.template} if self.template is not None else set()

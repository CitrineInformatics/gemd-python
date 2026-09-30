"""For entities that have specs."""

from abc import abstractmethod
from typing import Optional, Set, Type, Union

from gemd.entity.base_entity import BaseEntity
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.template.base_template import BaseTemplate

__all__ = ["HasSpec"]


class HasSpec(HasDependencies):
    """Mix-in trait for objects that can be assigned specs."""

    def __init__(self, spec: Union[HasTemplate, LinkByUID] = None):
        self._spec = None
        self.spec = spec

    @property
    def spec(self) -> Union[HasTemplate, LinkByUID]:
        """A spec, which expresses the anticipated or aspirational behavior of this object."""
        return self._spec

    @spec.setter
    def spec(self, spec: Union[HasTemplate, LinkByUID]):
        """Set the spec."""
        if spec is None:
            self._spec = None
        elif isinstance(spec, (self._spec_type(), LinkByUID)):
            self._spec = spec
        else:
            raise TypeError(
                f"Template must be a {self._spec_type()} or LinkByUID, not {type(spec)}"
            )

    @staticmethod
    @abstractmethod
    def _spec_type() -> Type:
        """Child must report implementation details."""

    @property
    def template(self) -> Optional[Union[BaseTemplate, LinkByUID]]:
        """The template that bounds this object.

        Objects that also mix in :class:`~gemd.entity.object.has_template.HasTemplate` return
        their own template when it is set.  Otherwise, this is the template of the spec, if the
        spec is an object that has one.
        """
        if isinstance(self, HasTemplate):
            own = HasTemplate.template.fget(self)
            if own is not None:
                return own
        if isinstance(self.spec, HasTemplate):
            return self.spec.template
        else:
            return None

    @template.setter
    def template(self, template: Optional[Union[BaseTemplate, LinkByUID]]):
        """Set the object's own template, if it can carry one."""
        if not isinstance(self, HasTemplate):
            raise AttributeError(f"{type(self).__name__} does not carry its own template.")
        HasTemplate.template.fset(self, template)

    def _local_dependencies(self) -> Set[Union[BaseEntity, LinkByUID]]:
        """Return a set of all immediate dependencies (no recursion)."""
        result = {self.spec} if self.spec is not None else set()
        if isinstance(self, HasTemplate):
            result |= HasTemplate._local_dependencies(self)
        return result

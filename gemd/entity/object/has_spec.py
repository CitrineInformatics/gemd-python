"""For entities that have specs."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.link_by_uid import LinkByUID

from abc import abstractmethod
from typing import Optional, Union, Set, Type


class HasSpec(HasDependencies):
    """Mix-in trait for objects that can be assigned specs.

    Parameters
    ----------
    spec: :class:`Has_Template <gemd.entity.object.has_template.Has_Template>`
        A spec, which expresses the anticipated or aspirational behavior of this object.

    """

    def __init__(self, spec: Union[HasTemplate, LinkByUID] = None):
        self._spec = None
        self.spec = spec

    @property
    def spec(self) -> Union[HasTemplate, LinkByUID]:
        """Get the spec."""
        return self._spec

    @spec.setter
    def spec(self, spec: Union[HasTemplate, LinkByUID]):
        """Set the spec."""
        if spec is None:
            self._spec = None
        elif isinstance(spec, (self._spec_type(), LinkByUID)):
            self._spec = spec
        else:
            raise TypeError(f"Template must be a {self._spec_type()} or LinkByUID, "
                            f"not {type(spec)}")

    @staticmethod
    @abstractmethod
    def _spec_type() -> Type:
        """Child must report implementation details."""

    @property
    def template(self) -> Optional[Union[BaseTemplate, LinkByUID]]:
        """Get the template associated with the spec."""
        if isinstance(self.spec, HasTemplate):
            return self.spec.template
        else:
            return None

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.spec} if self.spec is not None else set()

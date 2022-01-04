"""For entities that have templates."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger

from abc import abstractmethod
from inspect import getmodule, isclass
from typing import Optional, Union, Set, Type, Callable, TypeVar

T = TypeVar('T')


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

    def _generate_template_check(self,
                                 validate: Callable[[Union["HasSpec", "HasTemplate"], T], bool]
                                 ) -> Callable[[T], T]:
        """Generate a closure for the object and the validation routine."""
        from gemd.entity.object.has_spec import HasSpec

        if not isinstance(self, (HasSpec, HasTemplate)):
            raise ValueError(f"{self} does not support object template checks.")

        module = getmodule(validate)
        cls = None
        if module is not None:
            for member in module.__dict__.values():
                if isclass(member) and member.__module__ == module.__name__:
                    cls = member
                    break
        if cls is None:
            raise ValueError(f"Could not map class for function {validate}.")
        attr = next((y for x, y in validate.__annotations__.items() if x != 'return'), None)
        if attr is None:
            raise ValueError(f"Could not map attribute for function {validate}.")

        def template_check(x: attr) -> attr:
            level = get_validation_level()
            reject = level != WarningLevel.IGNORE \
                and isinstance(self.template, cls) \
                and not validate(self.template, x)

            if reject:
                message = f"Value {x.value} is inconsistent with template {self.template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)
            return x

        return template_check

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {self.template} if self.template is not None else set()

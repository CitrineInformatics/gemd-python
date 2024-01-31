"""For entities that have parameters."""
from gemd.entity.base_entity import BaseEntity
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.object.has_template_check_generator import HasTemplateCheckGenerator
from gemd.entity.template.has_parameter_templates import HasParameterTemplates
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.setters import validate_list

from typing import Union, Iterable, List, Set
from abc import ABC

__all__ = ["HasParameters"]


class HasParameters(HasTemplateCheckGenerator, HasDependencies, ABC):
    """Mixin-trait for entities that include parameters."""

    def __init__(self, parameters: Union[Parameter, Iterable[Parameter]]):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self) -> List[Parameter]:
        """A list of parameters associated with this entity."""
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: Union[Parameter, Iterable[Parameter]]):
        """Set the list of parameters."""
        checker = self._generate_template_check(HasParameterTemplates.validate_parameter)
        self._parameters = validate_list(parameters, Parameter, trigger=checker)

    def _local_dependencies(self) -> Set[Union[BaseEntity, LinkByUID]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {param.template for param in self.parameters if param.template is not None}

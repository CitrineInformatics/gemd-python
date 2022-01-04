"""For entities that have parameters."""
from gemd.entity.has_dependencies import HasDependencies
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.setters import validate_list

from typing import Union, Iterable, List, Set


class HasParameters(HasDependencies):
    """Mixin-trait for entities that include parameters.

    Parameters
    ----------
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`]
        A list of parameters associated with this entity.

    """

    def __init__(self, parameters: Iterable[Parameter]):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self) -> List[Parameter]:
        """Get the list of parameters."""
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: Iterable[Parameter]):
        """Set the list of parameters."""
        self._parameters = validate_list(parameters, Parameter)

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {param.template for param in self.parameters if param.template is not None}

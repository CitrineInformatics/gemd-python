"""For entities that have parameters."""
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.template.parameter_template import ParameterTemplate
from gemd.entity.setters import validate_list

from typing import Iterable, List, Set


class HasParameters(object):
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

    def all_dependencies(self) -> Set[ParameterTemplate]:
        """Return a set of all immediate dependencies (no recursion)."""
        return {param.template for param in self.parameters if param.template is not None}

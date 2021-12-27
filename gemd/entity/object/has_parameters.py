"""For entities that have parameters."""
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.setters import validate_list


class HasParameters(object):
    """Mixin-trait for entities that include parameters.

    Parameters
    ----------
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`]
        A list of parameters associated with this entity.

    """

    def __init__(self, parameters):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self):
        """Get the list of parameters."""
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Set the list of parameters."""
        self._parameters = validate_list(parameters, Parameter)

    def all_dependencies(self):
        """Return a set of all immediate dependencies (no recursion)."""
        return {param.template for param in self.parameters if param.template is not None}

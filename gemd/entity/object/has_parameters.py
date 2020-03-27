"""For entities that have parameters."""
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.setters import validate_list


class HasParameters(object):
    """Mixin-trait for entities that include parameters."""

    def __init__(self, parameters):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self):
        """Get the list of parameters."""
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = validate_list(parameters, Parameter)

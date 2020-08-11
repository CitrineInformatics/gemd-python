"""For entities that have a parameter template."""
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.parameter_template import ParameterTemplate
from gemd.entity.bounds.base_bounds import BaseBounds
from typing import Iterable


class HasParameterTemplates(object):
    """
    Mixin-trait for entities that include parameter templates.

    Parameters
    ----------
    parameters: List[(ParameterTemplate, BaseBounds)]
        A list of tuples containing this entity's parameter templates as well
        as any restrictions on those templates' bounds.

    """

    def __init__(self, parameters):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self):
        """
        Get the list of parameter template/bounds tuples.

        Returns
        -------
        List[(ParameterTemplate, bounds)]
            List of this entity's parameter template/bounds pairs

        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Set the list of parameter templates.

        Parameters
        ----------
        parameters: List[(ParameterTemplate, bounds)]
            A list of tuples containing this entity's parameter templates as well
            as any restrictions on those templates' bounds.

        Returns
        -------
        List[(ParameterTemplate, bounds)]
            List of this entity's parameter template/bounds pairs

        """
        if isinstance(parameters, Iterable):
            if any(isinstance(x, BaseBounds) for x in parameters):
                parameters = [parameters]  # It's a template/bounds tuple (probably)
        self._parameters = validate_list(parameters,
                                         (ParameterTemplate, LinkByUID, list, tuple),
                                         trigger=BaseTemplate._homogenize_ranges
                                         )

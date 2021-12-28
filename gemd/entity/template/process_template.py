"""A process template."""
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.has_condition_templates import HasConditionTemplates
from gemd.entity.template.has_parameter_templates import HasParameterTemplates


class ProcessTemplate(BaseTemplate, HasConditionTemplates, HasParameterTemplates):
    """
    A process template.

    Process templates are collections of condition and parameter templates that constrain the
    values of a measurement's condition and parameter attributes, and provide a common structure
    for describing similar measurements.

    Parameters
    ----------
    name: str, required
        The name of the process template.
    description: str, optional
        Long-form description of the process template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    allowed_names: List[str], optional
        The set of names that a process' ingredients are allowed to use in their name field.
    allowed_labels: List[str], optional
        The set of labels that a process' ingredients are allowed to use in their labels field.
    conditions: List[:class:`ConditionTemplate \
    <gemd.entity.template.condition_template.ConditionTemplate>`] or \
    List[:class:`ConditionTemplate <gemd.entity.template.condition_template.ConditionTemplate>`,\
     :py:class:`BaseBounds <gemd.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated conditions. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this condition.
    parameters: List[:class:`ParameterTemplate \
    <gemd.entity.template.parameter_template.ParameterTemplate>`] or \
    List[:class:`ParameterTemplate <gemd.entity.template.parameter_template.ParameterTemplate>`,\
     :py:class:`BaseBounds <gemd.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated parameters. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this parameter.

    """

    typ = "process_template"

    def __init__(self, name, *, description=None,
                 conditions=None, parameters=None,
                 allowed_names=None, allowed_labels=None,
                 uids=None, tags=None):
        BaseTemplate.__init__(self, name=name, description=description,
                              uids=uids, tags=tags)
        HasConditionTemplates.__init__(self, conditions)
        HasParameterTemplates.__init__(self, parameters)

        self._allowed_names = None
        self.allowed_names = allowed_names

        self._allowed_labels = None
        self.allowed_labels = allowed_labels

    @property
    def allowed_names(self):
        """Get the allowed names."""
        return self._allowed_names

    @allowed_names.setter
    def allowed_names(self, allowed_names):
        if allowed_names is None:
            self._allowed_names = validate_list([], str)
        else:
            self._allowed_names = validate_list(allowed_names, str)

    @property
    def allowed_labels(self):
        """Get the allowed labels."""
        return self._allowed_labels

    @allowed_labels.setter
    def allowed_labels(self, allowed_labels):
        if allowed_labels is None:
            self._allowed_labels = validate_list([], str)
        else:
            self._allowed_labels = validate_list(allowed_labels, str)

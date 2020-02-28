"""A process template."""
from taurus.entity.setters import validate_list
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.has_condition_templates import HasConditionTemplates
from taurus.entity.template.has_parameter_templates import HasParameterTemplates
from taurus.entity.object.process_spec import ProcessSpec


class ProcessTemplate(BaseTemplate, HasConditionTemplates, HasParameterTemplates):
    """
    A process template.

    Process templates are collections of condition and parameter templates that constrain the
    values of a measurement's condition and parameter attributes, and provide a common structure
    for describing similar measurements.

    Parameters
    ----------
    name: str, optional
        The name of the process template.
    description: str, optional
        Long-form description of the process template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    conditions: List[:class:`ConditionTemplate \
    <taurus.entity.template.condition_template.ConditionTemplate>`] or \
    List[:class:`ConditionTemplate <taurus.entity.template.condition_template.ConditionTemplate>`,\
     :py:class:`BaseBounds <taurus.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated conditions. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this condition.
    parameters: List[:class:`ParameterTemplate \
    <taurus.entity.template.parameter_template.ParameterTemplate>`] or \
    List[:class:`ParameterTemplate <taurus.entity.template.parameter_template.ParameterTemplate>`,\
     :py:class:`BaseBounds <taurus.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated parameters. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this parameter.

    """

    typ = "process_template"

    def __init__(
        self,
        name=None,
        description=None,
        conditions=None,
        parameters=None,
        allowed_names=None,
        allowed_labels=None,
        uids=None,
        tags=None,
    ):
        BaseTemplate.__init__(self, name, description, uids, tags)
        HasConditionTemplates.__init__(self, conditions)
        HasParameterTemplates.__init__(self, parameters)

        self._allowed_names = None
        self.allowed_names = allowed_names

        self._allowed_labels = None
        self.allowed_labels = allowed_labels

    def __call__(
        self,
        name=None,
        template=None,
        parameters=None,
        conditions=None,
        uids=None,
        tags=None,
        notes=None,
        file_links=None,
    ):
        """Produces a process spec that is linked to this process template."""

        if not name:  # inherit name from the template by default
            name = self.name
        if not template:  # link the process spec to this template by default
            template = self
        if not parameters:  # inherit the parameters from the template (empty values)
            parameters = [parameter_template() for parameter_template, bounds in self.parameters]
        if not conditions:  # inherit the conditions from the template (empty values)
            conditions = [condition_template() for condition_template, bounds in self.conditions]

        return ProcessSpec(
            name=name,
            template=template,
            parameters=parameters,
            conditions=conditions,
            uids=uids,
            tags=tags,
            notes=notes,
            file_links=file_links,
        )

    @property
    def allowed_names(self):
        """Get the allowed names."""
        return self._allowed_names

    @allowed_names.setter
    def allowed_names(self, allowed_names):
        # if none, leave as none; don't set to the empty set
        if allowed_names is None:
            self._allowed_names = allowed_names
        else:
            self._allowed_names = validate_list(allowed_names, str)

    @property
    def allowed_labels(self):
        """Get the allowed labels."""
        return self._allowed_labels

    @allowed_labels.setter
    def allowed_labels(self, allowed_labels):
        # if none, leave as none; don't set to the empty set
        if allowed_labels is None:
            self._allowed_labels = allowed_labels
        else:
            self._allowed_labels = validate_list(allowed_labels, str)

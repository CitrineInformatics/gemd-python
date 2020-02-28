"""A measurement template."""
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.has_condition_templates import HasConditionTemplates
from taurus.entity.template.has_parameter_templates import HasParameterTemplates
from taurus.entity.template.has_property_templates import HasPropertyTemplates
from taurus.entity.object.measurement_spec import MeasurementSpec


class MeasurementTemplate(
    BaseTemplate, HasPropertyTemplates, HasConditionTemplates, HasParameterTemplates
):
    """
    A measurement template.

    Measurement templates are collections of condition, parameter and property templates that
    constrain the values of a measurement's condition, parameter and property attributes, and
    provide a common structure for describing similar measurements.

    Parameters
    ----------
    name: str, optional
        The name of the measurement template.
    description: str, optional
        Long-form description of the measurement template.
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
    properties: List[:class:`PropertyTemplate \
    <taurus.entity.template.property_template.PropertyTemplate>`] or \
    List[:class:`PropertyTemplate <taurus.entity.template.property_template.PropertyTemplate>`,\
     :py:class:`BaseBounds <taurus.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated properties. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this property.

    """

    typ = "measurement_template"

    def __init__(
        self,
        name=None,
        description=None,
        properties=None,
        conditions=None,
        parameters=None,
        uids=None,
        tags=None,
    ):
        BaseTemplate.__init__(self, name, description, uids, tags)
        HasPropertyTemplates.__init__(self, properties)
        HasConditionTemplates.__init__(self, conditions)
        HasParameterTemplates.__init__(self, parameters)

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
        """Produces a measurement spec that is linked to this measurement template."""

        if not name:  # inherit name from the template by default
            name = self.name
        if not template:  # link the measurement spec to this template by default
            template = self
        if not parameters:  # inherit the parameters from the template (empty values)
            parameters = [parameter_template() for parameter_template, bounds in self.parameters]
        if not conditions:  # inherit the conditions from the template (empty values)
            conditions = [condition_template() for condition_template, bounds in self.conditions]

        return MeasurementSpec(
            name=name,
            template=template,
            parameters=parameters,
            conditions=conditions,
            uids=uids,
            tags=tags,
            notes=notes,
            file_links=file_links,
        )

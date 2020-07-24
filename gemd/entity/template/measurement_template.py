"""A measurement template."""
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.has_condition_templates import HasConditionTemplates
from gemd.entity.template.has_parameter_templates import HasParameterTemplates
from gemd.entity.template.has_property_templates import HasPropertyTemplates


class MeasurementTemplate(BaseTemplate,
                          HasPropertyTemplates, HasConditionTemplates, HasParameterTemplates):
    """
    A measurement template.

    Measurement templates are collections of condition, parameter and property templates that
    constrain the values of a measurement's condition, parameter and property attributes, and
    provide a common structure for describing similar measurements.

    Parameters
    ----------
    name: str, required
        The name of the measurement template.
    description: str, optional
        Long-form description of the measurement template.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
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
    properties: List[:class:`PropertyTemplate \
    <gemd.entity.template.property_template.PropertyTemplate>`] or \
    List[:class:`PropertyTemplate <gemd.entity.template.property_template.PropertyTemplate>`,\
     :py:class:`BaseBounds <gemd.entity.bounds.base_bounds.BaseBounds>`], optional
        Templates for associated properties. Each template can be provided by itself, or as a list
        with the second entry being a separate, *more restrictive* Bounds object that defines
        the limits of the value for this property.

    """

    typ = "measurement_template"

    def __init__(self, name, *, description=None,
                 properties=None, conditions=None, parameters=None,
                 uids=None, tags=None):
        BaseTemplate.__init__(self, name=name, description=description,
                              uids=uids, tags=tags)
        HasPropertyTemplates.__init__(self, properties)
        HasConditionTemplates.__init__(self, conditions)
        HasParameterTemplates.__init__(self, parameters)

# Tools to help build GEMD objects
from gemd.entity.object import ProcessSpec, ProcessRun, MaterialSpec, IngredientSpec, \
    MaterialRun, IngredientRun, MeasurementSpec, MeasurementRun
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_properties import HasProperties
from gemd.entity.attribute import Property, PropertyAndConditions, Condition, Parameter
from gemd.entity.attribute.base_attribute import BaseAttribute
from gemd.entity.template import PropertyTemplate, ParameterTemplate, ConditionTemplate, \
    MaterialTemplate, MeasurementTemplate, ProcessTemplate
from gemd.entity.bounds import RealBounds, IntegerBounds, CategoricalBounds, \
    CompositionBounds, MolecularStructureBounds
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.value import NominalReal, NominalInteger, NominalCategorical, \
    EmpiricalFormula, InChI, Smiles
from gemd.entity.value.continuous_value import ContinuousValue
from gemd.entity.value.base_value import BaseValue

from typing import Union, List


def make_node(name: str,
              *,
              process_name: str = None,
              process_template: ProcessTemplate = None,
              material_template: MaterialTemplate = None) -> MaterialRun:
    """
    Generate a material-process spec-run quadruple.

    Parameters
    ----------
    name: str
        Name of the MaterialRun and MaterialSpec.
    process_name: str
        Name of the ProcessRun and ProcessSpec.  Defaults to
        `process_template.name` if `process_template` is defined, else `name`.
    process_template: ProcessTemplate
        ProcessTemplate for the quadruple.
    material_template: MaterialTemplate
        MaterialTemplate for the quadruple.

    Returns
    --------
    MaterialRun
        A MaterialRun with linked processes, specs and templates

    """
    if process_name is None:
        if process_template is None:
            process_name = name
        else:
            process_name = process_template.name

    my_process_spec = ProcessSpec(
        name=process_name,
        template=process_template
    )

    my_process_run = ProcessRun(
        name=process_name,
        spec=my_process_spec
    )

    my_mat_spec = MaterialSpec(
        name=name,
        process=my_process_spec,
        template=material_template
    )

    my_mat_run = MaterialRun(
        name=name,
        process=my_process_run,
        spec=my_mat_spec
    )
    return my_mat_run


def add_edge(input_material: MaterialRun,
             output_material: MaterialRun,
             *,
             name: str = None,
             mass_fraction: Union[float, ContinuousValue] = None,
             number_fraction: Union[float, ContinuousValue] = None,
             volume_fraction: Union[float, ContinuousValue] = None,
             absolute_quantity: Union[int, float, ContinuousValue] = None,
             absolute_units: str = None,
             ) -> IngredientRun:
    """
    Connect two material-process spec-run quadruples with ingredients.

    Parameters
    ----------
    input_material: MaterialRun
        The `material` for the returned IngredientRun
    output_material: MaterialRun
        The `process` for the returned IngredientRun will be
        `output_material.process`
    name: str
        The ingredient name.  Defaults to `input_material.name`.
    mass_fraction: float or ContinuousValue
        The mass fraction of the Ingredient Run.  0 <= x <= 1
    number_fraction: float or ContinuousValue
        The number fraction of the Ingredient Run.  0 <= x <= 1
    volume_fraction: float or ContinuousValue
        The volume fraction of the Ingredient Run.  0 <= x <= 1
    absolute_quantity: float or ContinuousValue
        The absolute quantity.  0 <= x
    absolute_units: str
        The absolute units.  Required if absolute_quantity is provided as a float

    Returns
    --------
    IngredientRun
        A IngredientRun with linked processes, specs and materials

    """
    output_spec = output_material.spec
    if not isinstance(output_spec, MaterialSpec) \
            or output_spec.process is None \
            or output_material.process is None:
        raise ValueError("Output Material must be a MaterialRun with connected "
                         "Specs and Processes.")
    if input_material.spec is None:
        raise ValueError("Input Material must be a MaterialRun with connected Spec.")

    if name is None:
        name = input_material.name
    my_ingredient_spec = IngredientSpec(name=name,
                                        process=output_spec.process,
                                        material=input_material.spec
                                        )
    my_ingredient_run = IngredientRun(spec=my_ingredient_spec,
                                      process=output_material.process,
                                      material=input_material
                                      )

    if mass_fraction is not None:
        if isinstance(mass_fraction, float):
            mass_fraction = NominalReal(nominal=mass_fraction, units='')
        my_ingredient_run.mass_fraction = mass_fraction

    if number_fraction is not None:
        if isinstance(number_fraction, float):
            number_fraction = NominalReal(nominal=number_fraction, units='')
        my_ingredient_run.number_fraction = number_fraction

    if volume_fraction is not None:
        if isinstance(volume_fraction, float):
            volume_fraction = NominalReal(nominal=volume_fraction, units='')
        my_ingredient_run.volume_fraction = volume_fraction

    if absolute_quantity is not None:
        if isinstance(absolute_quantity, float):
            if absolute_units is None:
                raise ValueError("Absolute Units are required if Absolute Quantity is not a Value")
            absolute_quantity = NominalReal(nominal=absolute_quantity, units=absolute_units)
            absolute_units = None
        my_ingredient_run.absolute_quantity = absolute_quantity

    if absolute_units is not None:
        raise ValueError("Absolute Units are only used if "
                         "Absolute Quantity is given as is a float.")

    return my_ingredient_run


def add_measurement(material: MaterialRun,
                    *,
                    name: str = None,
                    template: MeasurementTemplate = None,
                    attributes: List[BaseAttribute] = None,
                    ) -> MeasurementRun:
    """
    Add a measurement run-spec set to a MaterialRun.

    Parameters
    ----------
    material: MaterialRun
        The `material` for the returned MeasurementRun
    name: str
        The name of the measurement.  Defaults to
        `template.name` if `template` is defined.
    template: MeasurementTemplate
        The MeasurementTemplate.
    attributes: List[BaseAttribute]
        Attributes you want associated with this MeasurementRun.

    Returns
    --------
    MeasurementRun
        A MeasurementRun with linked material, spec and template

    """
    if name is None:
        if template is None:
            raise ValueError("Either a name or a template must be provided")
        else:
            name = template.name

    my_measurement_spec = MeasurementSpec(name, template=template)
    my_measurement_run = MeasurementRun(name, spec=my_measurement_spec, material=material)

    if attributes is not None:
        for attribute in attributes:
            if isinstance(attribute, Property):
                my_measurement_run.properties.append(attribute)
            elif isinstance(attribute, Condition):
                my_measurement_run.conditions.append(attribute)
            elif isinstance(attribute, Parameter):
                my_measurement_run.parameters.append(attribute)
            else:
                raise ValueError(f"Unhandled Attribute type {type(attribute)}")

    return my_measurement_run


def add_attribute(target: Union[HasProperties, HasConditions, HasParameters],
                  template: Union[PropertyTemplate, ConditionTemplate, ParameterTemplate],
                  value: Union[BaseValue, str, float, int]
                  ) -> Union[Property, Condition, Parameter]:
    """
    Generate an attribute, and then add it attribute to a GEMD object.

    Parameters
    ----------
    target: BaseObject
        The object to attach the attribute to
    template: AttributeTemplate
        The AttributeTemplate for the attribute.
    value: Union[BaseValue, str, float, int]
        The value for the attribute.  Accepts any GEMD Value type, or will
        attempt to generate an appropriate Value given a str, float or int.

    Returns
    --------
    BaseAttribute
        The generated attribute

    """
    attribute = make_attribute(template=template, value=value)
    attr_class = type(attribute)

    if isinstance(target, MaterialSpec):
        if attr_class is Property:
            target.properties.append(PropertyAndConditions(property=attribute))
        elif attr_class is Condition:
            if len(target.properties) == 0:
                raise ValueError("Cannot add a condition to a MaterialSpec "
                                 "before it has at least one property.")
            target.properties[-1].conditions.append(attribute)
        else:
            raise ValueError(f"Attribute {attr_class} is incompatible with target {type(target)}.")
    else:  # All other target types
        if attr_class is Property and isinstance(target, HasProperties):
            target.properties.append(attribute)
        elif attr_class is Condition and isinstance(target, HasConditions):
            target.conditions.append(attribute)
        elif attr_class is Parameter and isinstance(target, HasParameters):
            target.parameters.append(attribute)
        else:
            raise ValueError(f"A {attr_class} cannot be added to a {type(target)}.")

    return attribute


def make_attribute(template: Union[PropertyTemplate, ConditionTemplate, ParameterTemplate],
                   value: Union[BaseValue, str, float, int]
                   ) -> Union[Property, Condition, Parameter]:
    """
    Generate an Attribute and the contained Value.

    Parameters
    ----------
    template: AttributeTemplate
        The AttributeTemplate for the attribute.
    value: Union[BaseValue, str, float, int]
        The value for the attribute.  Accepts any GEMD Value type, or will
        attempt to generate an appropriate Value given a str, float or int.

    Returns
    --------
    BaseAttribute
        The generated attribute

    """
    if isinstance(template, PropertyTemplate):
        attr_class = Property
    elif isinstance(template, ConditionTemplate):
        attr_class = Condition
    elif isinstance(template, ParameterTemplate):
        attr_class = Parameter
    else:
        raise ValueError(f"Unrecognized attribute template type {type(template)}")

    if not isinstance(value, BaseValue):
        value = make_value(value, template.bounds)

    attribute = attr_class(name=template.name, value=value, template=template)

    return attribute


def make_value(value: Union[str, float, int],
               bounds: BaseBounds) -> BaseValue:
    """
    Generate a Value object based upon a number or string and a particular bounds.

    Parameters
    ----------
    value: Union[str, float, int]
        The primitive type to wrap in a Value
    bounds: BaseBounds
        The bounds type to determine which value type we want to coerce the value into

    Returns
    --------
    BaseValue
        The generated value

    """
    if isinstance(bounds, RealBounds):
        result = NominalReal(value, units=bounds.default_units)
    elif isinstance(bounds, IntegerBounds):
        result = NominalInteger(value)
    elif isinstance(bounds, CategoricalBounds):
        result = NominalCategorical(value)
    elif isinstance(bounds, CompositionBounds):
        result = EmpiricalFormula(value)
    elif isinstance(bounds, MolecularStructureBounds):
        if str(value).startswith("InChI="):
            result = InChI(value)
        else:
            result = Smiles(value)
    else:
        raise ValueError(f"Unrecognized bound type in template {type(bounds)}")

    return result

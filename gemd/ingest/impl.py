# Tools to help build GEMD objects
from gemd.entity.object import ProcessSpec, ProcessRun, MaterialSpec, IngredientSpec, \
    MaterialRun, IngredientRun, MeasurementSpec, MeasurementRun
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_properties import HasProperties
from gemd.entity.attribute import Property, PropertyAndConditions, Condition, Parameter
from gemd.entity.template import PropertyTemplate, ParameterTemplate, ConditionTemplate, \
    MaterialTemplate, MeasurementTemplate, ProcessTemplate
from gemd.entity.template.attribute_template import AttributeTemplate
from gemd.entity.bounds import RealBounds, IntegerBounds, CategoricalBounds, \
    CompositionBounds, MolecularStructureBounds
from gemd.entity.value import NominalReal, NominalInteger, NominalCategorical, \
    EmpiricalFormula, Smiles
from gemd.entity.value.base_value import BaseValue
from typing import Union


def make_node(name: str,
              *,
              process_name: str = None,
              process_template: ProcessTemplate = None,
              material_template: MaterialTemplate = None):
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
             name: str = None):
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

    Returns
    --------
    MaterialRun
        A MaterialRun with linked processes, specs and templates

    """
    if name is None:
        name = input_material.name
    my_ingredient_spec = IngredientSpec(name=name,
                                        process=output_material.spec.process,
                                        material=input_material.spec
                                        )
    my_ingredient_spec = IngredientRun(spec=my_ingredient_spec,
                                       process=output_material.process,
                                       material=input_material
                                       )
    return my_ingredient_spec


def add_measurement(material: MaterialRun,
                    name: str = None,
                    *,
                    template: MeasurementTemplate = None
                    ):
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

    return my_measurement_run


def add_attribute(target: Union[HasConditions, HasParameters, HasProperties],
                  template: AttributeTemplate,
                  value: Union[BaseValue, str, float, int]):
    """
    Add an attribute to a GEMD object.

    Parameters
    ----------
    target: BaseObejct
        The object to attach the attribute to
    template: AttributeTemplate
        The AttributeTemplate for the attribute.
    value: Union[BaseValue, str, float, int])
        The value for the attribute.  Accepts any GEMD Value type, or will
        attempt to generate an appropriate Value given a str, float or int.

    Returns
    --------
    BaseAttribute
        The generated attribute

    """
    attr_class = Property if isinstance(template, PropertyTemplate) else \
        Condition if isinstance(template, ConditionTemplate) else \
        Parameter if isinstance(template, ParameterTemplate) else \
        None
    if not isinstance(value, BaseValue):
        if isinstance(template.bounds, RealBounds):
            value = NominalReal(value, units=template.bounds.default_units)
        elif isinstance(template.bounds, IntegerBounds):
            value = NominalInteger(value)
        elif isinstance(template.bounds, CategoricalBounds):
            value = NominalCategorical(value)
        elif isinstance(template.bounds, CompositionBounds):
            value = EmpiricalFormula(value)
        elif isinstance(template.bounds, MolecularStructureBounds):
            value = Smiles(value)
        else:
            raise ValueError(f"Unrecognized bound type in template {type(template.bounds)}")

    attribute = attr_class(name=template.name, value=value, template=template)

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
        try:
            lst = target.properties if attr_class is Property else \
                target.conditions if attr_class is Condition else \
                target.parameters if attr_class is Parameter else \
                None
            lst.append(attribute)
        except AttributeError:
            raise ValueError(f"A {attr_class} cannot be added to a {type(target)}.")

    return attribute

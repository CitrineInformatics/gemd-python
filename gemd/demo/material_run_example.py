"""An example ingest of a material run."""
from gemd import units
from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.attribute.property import Property
from gemd.entity.bounds.categorical_bounds import CategoricalBounds
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.object import MaterialRun, MeasurementRun
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.template.parameter_template import ParameterTemplate
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.value.discrete_categorical import DiscreteCategorical
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.value.normal_real import NormalReal

known_properties = {
    "density": PropertyTemplate(
        name="density",
        bounds=RealBounds(lower_bound=0.0, upper_bound=1000.0, default_units='g / cm^3')
    ),
    "kinematic viscosity": PropertyTemplate(
        name="kinematic viscosity",
        bounds=RealBounds(lower_bound=0.0, upper_bound=10.0**40, default_units="m^2 / s")
    )
}

known_conditions = {
    "temperature": ConditionTemplate(
        name="temperature",
        bounds=RealBounds(lower_bound=0.0, upper_bound=1000.0, default_units='K')
    )
}

known_parameters = {
    "knob_2_setting": ParameterTemplate(
        name="knob_2_setting",
        bounds=CategoricalBounds(categories={"low", "medium", "high"})
    )
}


def _parse_value(val):
    """Example field-parsing logic."""
    # If the string is complicated, split it up and try to get uncertainty and/or units
    if isinstance(val, str) and len(val.split()) > 1:
        toks = val.split()
        mean = float(toks[0])
        std = -1
        if toks[1] in {"+-", "+/-"}:
            std = float(toks[2])

        try:
            unit = units.parse_units(toks[-1])
        except (ValueError, units.UndefinedUnitError):
            print("Couldn't find {}".format(toks[-1]))
            unit = ''

        if std >= 0:
            return NormalReal(mean=mean, std=std, units=unit)
        else:
            return NominalReal(mean, units=unit)
    # if it is just a number wrap it in a nominal value
    elif isinstance(val, (float, int)):
        return NominalReal(val, '')
    # if it is a single string, it's either a single number of a category
    elif isinstance(val, str):
        try:
            num = float(val)
            return NominalReal(num, '')
        except ValueError:
            return DiscreteCategorical(val)
    else:
        raise ValueError("Couldn't parse {}".format(val))


def ingest_material_run(data, material_spec=None, process_run=None):
    """Ingest material run with data, a material spec, and an originating process run."""
    if isinstance(data, list):
        return [ingest_material_run(x, material_spec) for x in data]

    if not isinstance(data, dict):
        raise ValueError("This ingester operates on dict, but got {}".format(type(data)))

    material = MaterialRun("Material Run")

    sample_id = data.get("sample_id")
    if sample_id:
        material.add_uid("given_sample_id", sample_id)

    tags = data.get("tags")
    if tags:
        material.tags = tags

    for experiment in data.get("experiments", []):
        measurement = MeasurementRun("Measurement Run")

        for name in set(known_properties.keys()).intersection(experiment.keys()):
            prop = Property(
                name=name,
                template=known_properties[name],
                value=_parse_value(experiment[name])
            )
            measurement.properties.append(prop)

        for name in set(known_conditions.keys()).intersection(experiment.keys()):
            cond = Condition(
                name=name,
                template=known_conditions[name],
                value=_parse_value(experiment[name])
            )
            measurement.conditions.append(cond)

        for name in set(known_parameters.keys()).intersection(experiment.keys()):
            param = Parameter(
                name=name,
                template=known_parameters[name],
                value=_parse_value(experiment[name])
            )
            measurement.parameters.append(param)

        scan_id = experiment.get("scan_id")
        if scan_id:
            measurement.add_uid("given_scan_id", scan_id)

        tags = experiment.get("tags")
        if tags:
            measurement.tags = tags

        measurement.material = material

    if material_spec:
        material.material_spec = material_spec

    if process_run:
        material.process = process_run

    return material

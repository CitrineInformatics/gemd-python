"""Test of a complicated set of interlocking data objects."""
import json

from taurus.entity.object.ingredient_run import IngredientRun
from toolz import keymap, merge, keyfilter

from taurus.client.json_encoder import dumps
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.attribute.property import Property
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.object import MeasurementRun, MaterialRun, ProcessRun, ProcessSpec,\
    MeasurementSpec, MaterialSpec
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate
from taurus.entity.template.process_template import ProcessTemplate
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_composition import NominalComposition
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.entity.value.uniform_real import UniformReal

density_template = PropertyTemplate(
    name="Density",
    bounds=RealBounds(lower_bound=0, upper_bound=1.0e9, default_units='')
)
firing_temperature_template = ConditionTemplate(
    name="Firing Temperature",
    bounds=RealBounds(lower_bound=0, upper_bound=1.0e9, default_units='degC')
)

measurement_template = MeasurementTemplate(properties=density_template)
firing_template = ProcessTemplate(
    name="Firing in a kiln",
    conditions=(firing_temperature_template, RealBounds(lower_bound=500, upper_bound=1000,
                                                        default_units='degC'))
)
material_template = MaterialTemplate(
    name="Some ceramic thing",
    properties=density_template
)


def make_data_island(density, bulk_modulus, firing_temperature, binders, powders, tag=None):
    """Helper function to create a relatively involved data island."""
    binder_specs = keymap(lambda x: MaterialSpec(name=x), binders)
    powder_specs = keymap(lambda x: MaterialSpec(name=x), powders)

    binder_runs = keymap(lambda x: MaterialRun(spec=x), binder_specs)
    powder_runs = keymap(lambda x: MaterialRun(spec=x), powder_specs)

    binder_ingredients = []
    for run in binder_runs:
        binder_ingredients.append(
            IngredientRun(
                material=run,
                mass_fraction=NominalReal(binders[run.spec.name], ''),
                name=run.spec.name,
                labels=["binder"]
            )
        )

    powder_ingredients = []
    for run in powder_runs:
        powder_ingredients.append(
            IngredientRun(
                material=run,
                mass_fraction=NominalReal(powders[run.spec.name], ''),
                name=run.spec.name,
                labels=["powder"]
            )
        )

    all_input_materials = merge(binder_runs, powder_runs)
    all_ingredients = binder_ingredients + powder_ingredients

    mixing_composition = Condition(
        name="composition",
        value=NominalComposition(all_input_materials)
    )
    mixing_process = ProcessRun(
        tags=["mixing"],
        ingredients=all_ingredients,
        conditions=[mixing_composition]
    )

    green_sample = MaterialRun(process=mixing_process)

    measured_firing_temperature = Condition(
        name="Firing Temperature",
        value=UniformReal(firing_temperature - 0.5, firing_temperature + 0.5, 'degC'),
        template=firing_temperature_template
    )

    specified_firing_setting = Parameter(
        name="Firing setting",
        value=DiscreteCategorical("hot")
    )
    firing_spec = ProcessSpec(template=firing_template)
    firing_process = ProcessRun(
        conditions=[measured_firing_temperature],
        parameters=[specified_firing_setting],
        ingredients=[IngredientRun(
            green_sample,
            mass_fraction=NormalReal(1.0, 0.0, ''),
            volume_fraction=NormalReal(1.0, 0.0, ''),
            number_fraction=NormalReal(1.0, 0.0, '')
        )],
        spec=firing_spec
    )

    measured_density = Property(
        name="Density",
        value=NominalReal(density, ''),
        template=density_template
    )
    measured_modulus = Property(
        name="Bulk modulus",
        value=NormalReal(bulk_modulus, bulk_modulus / 100.0, '')
    )
    measurement_spec = MeasurementSpec(template=measurement_template)
    measurement = MeasurementRun(
        properties=[measured_density, measured_modulus],
        spec=measurement_spec
    )

    if tag:
        tags = [tag]
    else:
        tags = []

    material_spec = MaterialSpec(template=material_template)
    material_run = MaterialRun(process=firing_process, tags=tags, spec=material_spec)
    measurement.material = material_run
    return material_run


def test_access_data():
    """Demonstrate and test access patterns within the data island."""
    binders = {
        "Polyethylene Glycol 100M": 0.02,
        "Sodium lignosulfonate": 0.004,
        "Polyvinyl Acetate": 0.0001
    }
    powders = {"Al2O3": 0.96}
    island = make_data_island(
        density=1.0,
        bulk_modulus=300.0,
        firing_temperature=750.0,
        binders=binders,
        powders=powders,
        tag="Me"
    )

    # read the density value
    assert(island.measurements[0].properties[0].value == NominalReal(1.0, ''))
    # read the bulk modulus value
    assert(island.measurements[0].properties[1].value == NormalReal(300.0, 3.0, ''))
    # read the firing temperature
    assert(island.process.conditions[0].value == UniformReal(749.5, 750.5, 'degC'))
    assert(island.process.parameters[0].value == DiscreteCategorical({"hot": 1.0}))

    # read the quantity of alumina
    quantities = island.process.ingredients[0].material.process.conditions[0].value.quantities
    assert(list(
        keyfilter(lambda x: x.spec.name == "Al2O3", quantities).values()
    )[0] == 0.96)

    # check that the serialization results in the correct number of objects in the preface
    # (note that measurements are not serialized)
    assert(len(json.loads(dumps(island))[0]) == 23)

"""Test of a complicated set of interlocking data objects."""
import json as json_builtin
import gemd.json as gemd_json

from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.attribute.property import Property
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.object import MeasurementRun, MaterialRun, ProcessRun, ProcessSpec,\
    MeasurementSpec, MaterialSpec, IngredientRun
from gemd.entity.template.condition_template import ConditionTemplate
from gemd.entity.template.material_template import MaterialTemplate
from gemd.entity.template.measurement_template import MeasurementTemplate
from gemd.entity.template.process_template import ProcessTemplate
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.value.discrete_categorical import DiscreteCategorical
from gemd.entity.value.nominal_composition import NominalComposition
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.value.normal_real import NormalReal
from gemd.entity.value.uniform_real import UniformReal

density_template = PropertyTemplate(
    name="Density",
    bounds=RealBounds(lower_bound=0, upper_bound=1.0e9, default_units='')
)
firing_temperature_template = ConditionTemplate(
    name="Firing Temperature",
    bounds=RealBounds(lower_bound=0, upper_bound=1.0e9, default_units='degC')
)

measurement_template = MeasurementTemplate("Density Measurement", properties=density_template)
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
    binder_specs = {MaterialSpec(name=k): v for k, v in binders.items()}
    powder_specs = {MaterialSpec(name=k): v for k, v in powders.items()}

    binder_runs = {MaterialRun(name=k.name, spec=k): v for k, v in binder_specs.items()}
    powder_runs = {MaterialRun(name=k.name, spec=k): v for k, v in powder_specs.items()}

    all_input_materials = {k.spec.name: v for k, v in binder_runs.items() | powder_runs.items()}
    mixing_composition = Condition(
        name="composition",
        value=NominalComposition(all_input_materials)
    )
    mixing_process = ProcessRun(
        name="Mixing",
        tags=["mixing"],
        conditions=[mixing_composition]
    )
    binder_ingredients = []
    for run in binder_runs:
        binder_ingredients.append(
            IngredientRun(
                material=run,
                process=mixing_process,
                mass_fraction=NominalReal(binders[run.spec.name], ''),
            )
        )

    powder_ingredients = []
    for run in powder_runs:
        powder_ingredients.append(
            IngredientRun(
                material=run,
                process=mixing_process,
                mass_fraction=NominalReal(powders[run.spec.name], ''),
            )
        )

    green_sample = MaterialRun("Green", process=mixing_process)

    measured_firing_temperature = Condition(
        name="Firing Temperature",
        value=UniformReal(firing_temperature - 0.5, firing_temperature + 0.5, 'degC'),
        template=firing_temperature_template
    )

    specified_firing_setting = Parameter(
        name="Firing setting",
        value=DiscreteCategorical("hot")
    )
    firing_spec = ProcessSpec("Firing", template=firing_template)
    firing_process = ProcessRun(
        name=firing_spec.name,
        conditions=[measured_firing_temperature],
        parameters=[specified_firing_setting],
        spec=firing_spec
    )
    IngredientRun(
        material=green_sample,
        process=firing_process,
        mass_fraction=NormalReal(1.0, 0.0, ''),
        volume_fraction=NormalReal(1.0, 0.0, ''),
        number_fraction=NormalReal(1.0, 0.0, '')
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
    measurement_spec = MeasurementSpec("Mechanical Properties",
                                       template=measurement_template)
    measurement = MeasurementRun(
        measurement_spec.name,
        properties=[measured_density, measured_modulus],
        spec=measurement_spec
    )

    tags = [tag] if tag else []

    material_spec = MaterialSpec("Coupon", template=material_template)
    material_run = MaterialRun(material_spec.name, process=firing_process,
                               tags=tags, spec=material_spec)
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
    assert quantities.get("Al2O3") == 0.96

    # check that the serialization results in the correct number of objects in the preface
    # (note that neither measurements nor ingredients are serialized)
    assert(len(json_builtin.loads(gemd_json.dumps(island))["context"]) == 26)

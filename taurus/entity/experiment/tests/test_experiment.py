from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate
from taurus.entity.template.process_template import ProcessTemplate

from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.parameter_template import ParameterTemplate

from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.real_bounds import RealBounds

from taurus.entity.experiment.experiment_template import ExperimentTemplate

import taurus.util.impl as utils

# property templates
conductivity = PropertyTemplate(
    name="conductivity",
    bounds=RealBounds(lower_bound=0, upper_bound=100000, default_units="S/m"),
)
seebeck = PropertyTemplate(
    name="Seebeck", bounds=RealBounds(lower_bound=-500, upper_bound=500, default_units="uV/K"),
)

# condition templates
atmosphere = ConditionTemplate(name="atmosphere", bounds=CategoricalBounds(["air", "argon"]))
pressure = ConditionTemplate(
    name="pressure", bounds=RealBounds(lower_bound=0, upper_bound=1, default_units="atm")
)
day_of_the_week = ConditionTemplate(
    name="day of the week", bounds=CategoricalBounds(["M", "T", "W", "Th", "F"])
)

# parameter templates
vendor = ParameterTemplate(
    name="vendor", bounds=CategoricalBounds(["alpha-aesar", "sigma-aldrich"])
)
field_strength = ParameterTemplate(
    name="field_strength", bounds=RealBounds(lower_bound=0, upper_bound=5, default_units="T"),
)
temperature = ParameterTemplate(
    name="temperaure", bounds=RealBounds(lower_bound=300, upper_bound=1000, default_units="K")
)

# object templates
material = MaterialTemplate(name="test material", properties=[conductivity, seebeck])
measurement = MeasurementTemplate(
    name="test measurement",
    properties=[conductivity, seebeck],
    conditions=[atmosphere, pressure],
    parameters=[field_strength],
)
procure = ProcessTemplate(name="procure", conditions=[day_of_the_week], parameters=[vendor])
heat_treat = ProcessTemplate(
    name="heat treat", conditions=[atmosphere], parameters=[temperature]
)

templates = {
    "procure": procure,
    "initial_sample": material,
    "initial_measurement": measurement,
    "heat_treat": heat_treat,
    "treated_sample": material,
    "treated_measurement": measurement,
}
connections = [
    ("procure", "initial_sample"),
    ("initial_sample", "initial_measurement"),
    ("initial_sample", "heat_treat"),
    ("heat_treat", "treated_sample"),
    ("treated_sample", "treated_measurement"),
]

template_model = ExperimentTemplate(objects=templates, connections=connections)
spec_model = template_model()
run_model = spec_model()
run_model.visualize()
entities = utils.flatten(run_model.objects['treated_sample'])

print(len(entities))

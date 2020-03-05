from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate
from taurus.entity.template.process_template import ProcessTemplate

from taurus.entity.object.ingredient_spec import IngredientSpec

from taurus.entity.experiment.base_experiment import BaseExperiment


class ExperimentTemplate(BaseExperiment):
    """An experiment template is a collection of Taurus templates, with connections between them.
    """

    def __init__(self, objects, connections, uids, tags):
        BaseExperiment.__init__(
            self, objects=objects, connections=connections, uids=uids, tags=tags
        )

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        for obj in objects.values():
            assert isinstance(obj, BaseTemplate)
        self._objects = objects

    def __call__(self):
        """Create a spec state of this template model."""
        from taurus.entity.experiment.experiment_spec import ExperimentSpec

        specs = dict()
        connections = list()

        # first, add processes to the specs collection
        for key, template in self.objects.items():
            if isinstance(template, ProcessTemplate):
                specs[key] = template()  # creates a spec from template

        # second, add materials which are linked to process specs
        for key, template in self.objects.items():
            if isinstance(template, MaterialTemplate):
                creating_process = [
                    source for source, destination in self.connections if destination == key
                ][0]
                specs[key] = template(process=specs[creating_process])
                connections.append((creating_process, key))

        # third, add ingredients that feed into processes
        infered_ingredients = []
        for source, destination in self.connections:
            if isinstance(self.objects[source], MaterialTemplate) & isinstance(
                self.objects[destination], ProcessTemplate
            ):
                infered_ingredients.append((source, destination))
        for material, process in infered_ingredients:
            ingredient_name = "ingredient: {}".format(material)
            specs[ingredient_name] = IngredientSpec(
                name=ingredient_name, material=specs[material], process=specs[process]
            )
            connections.append((material, ingredient_name))
            connections.append((ingredient_name, process))

        # fourth, add measurements attached to materials
        for key, template in self.objects.items():
            if isinstance(template, MeasurementTemplate):
                specs[key] = template()

        return ExperimentSpec(
            objects=specs,
            connections=connections,
            uids=self.uids,
            tags=self.tags,
            template_model=self,
        )


if __name__ == "__main__":
    from taurus.entity.template.property_template import PropertyTemplate
    from taurus.entity.template.condition_template import ConditionTemplate
    from taurus.entity.template.parameter_template import ParameterTemplate

    from taurus.entity.bounds.categorical_bounds import CategoricalBounds
    from taurus.entity.bounds.real_bounds import RealBounds

    from taurus.util.impl import flatten

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

    data_model = TemplateModel(templates=templates, connections=connections)
    data_model.visualize()

    specs, connections = data_model.spec
    print(flatten(specs["treated_sample"]))

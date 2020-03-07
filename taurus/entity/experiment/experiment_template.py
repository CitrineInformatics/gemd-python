from taurus.entity.experiment.base_experiment import BaseExperiment

from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate
from taurus.entity.template.process_template import ProcessTemplate


ALLOWED_CONNECTION_TYPES = [
    (ProcessTemplate, MaterialTemplate),
    (MaterialTemplate, ProcessTemplate),
    (MaterialTemplate, MeasurementTemplate),
]


class ExperimentTemplate(BaseExperiment):
    """An experiment template is a collection of Taurus templates, with connections between them.
    """

    def __init__(self, objects, connections, uids=None, tags=None):
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

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def connections(self, connections):
        for source, destination in connections:
            assert source in self.objects.keys()
            assert destination in self.objects.keys()
            assert (
                type(self.objects[source]),
                type(self.objects[destination]),
            ) in ALLOWED_CONNECTION_TYPES
        self._connections = connections

    def __call__(self):
        """Create a spec state of this template model."""
        from taurus.entity.experiment.experiment_spec import ExperimentSpec
        from taurus.entity.object.ingredient_spec import IngredientSpec
        # TODO: make this more paletale, and use uids and tags
        # Diddo with the ExperimentSpec __call__ method

        specs = dict()
        connections = list()

        # first, add processes to the specs collection
        for key, template in self.objects.items():
            if isinstance(template, ProcessTemplate):
                specs[key] = template(name=key)  # creates a spec from template

        # second, add materials which are linked to process specs
        for key, template in self.objects.items():
            if isinstance(template, MaterialTemplate):
                creating_process = [
                    source for source, destination in self.connections if destination == key
                ][0]
                specs[key] = template(name=key, process=specs[creating_process])
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
                attached_material = [
                    source for source, destination in self.connections if destination == key
                ][0]
                specs[key] = template(name=key)
                connections.append((attached_material, key))

        return ExperimentSpec(
            objects=specs, connections=connections, template=self, uids=self.uids, tags=self.tags,
        )

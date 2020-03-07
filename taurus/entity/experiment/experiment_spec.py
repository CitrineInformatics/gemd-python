from taurus.entity.experiment.base_experiment import BaseExperiment

from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.process_spec import ProcessSpec


ALLOWED_CONNECTION_TYPES = [
    (ProcessSpec, MaterialSpec),
    (MaterialSpec, IngredientSpec),
    (IngredientSpec, ProcessSpec),
    (MaterialSpec, MeasurementSpec),
]


class ExperimentSpec(BaseExperiment):
    """An experiment spec is a collection of Taurus spec objects, with connections between them.
    """

    def __init__(self, objects, connections, template, uids=None, tags=None):
        BaseExperiment.__init__(
            self, objects=objects, connections=connections, uids=uids, tags=tags
        )
        self._template = None
        self.template = template

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        for obj in objects.values():
            assert isinstance(obj, (IngredientSpec, MaterialSpec, MeasurementSpec, ProcessSpec))
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

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        from taurus.entity.experiment.experiment_template import ExperimentTemplate
        assert isinstance(template, ExperimentTemplate)
        self._template = template

    def __call__(self):
        """Create a spec state of this template model."""
        from taurus.entity.experiment.experiment_run import ExperimentRun

        runs = dict()
        connections = list()

        # first, add processes to the runs collection
        for key, spec in self.objects.items():
            if isinstance(spec, ProcessSpec):
                runs[key] = spec()  # creates a spec from spec

        # second, add materials which are linked to process runs
        for key, spec in self.objects.items():
            if isinstance(spec, MaterialSpec):
                creating_process = [
                    source for source, destination in self.connections if destination == key
                ][0]
                runs[key] = spec(process=runs[creating_process])
                connections.append((creating_process, key))

        # third, add ingredients that feed into processes
        for key, spec in self.objects.items():
            if isinstance(spec, IngredientSpec):
                material = [
                    source for source, destination in self.connections if destination == key
                ][0]
                process = [
                    destination for source, destination in self.connections if source == key
                ][0]
                runs[key] = spec(process=runs[process], material=runs[material])
                connections.append((material, key))
                connections.append((key, process))

        # fourth, add measurements attached to materials
        for key, spec in self.objects.items():
            if isinstance(spec, MeasurementSpec):
                attached_material = [
                    source for source, destination in self.connections if destination == key
                ][0]
                runs[key] = spec(material=runs[attached_material])
                connections.append((attached_material, key))

        return ExperimentRun(
            objects=runs, connections=connections, spec=self, uids=self.uids, tags=self.tags,
        )

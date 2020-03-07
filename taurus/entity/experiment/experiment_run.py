from taurus.entity.experiment.base_experiment import BaseExperiment

from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.process_run import ProcessRun


ALLOWED_CONNECTION_TYPES = [
    (ProcessRun, MaterialRun),
    (MaterialRun, IngredientRun),
    (IngredientRun, ProcessRun),
    (MaterialRun, MeasurementRun),
]


class ExperimentRun(BaseExperiment):
    """An experiment run is a collection of Taurus run objects, with connections between them.
    """

    def __init__(self, objects, connections, spec, uids=None, tags=None):
        BaseExperiment.__init__(
            self, objects=objects, connections=connections, uids=uids, tags=tags
        )
        self._spec = None
        self.spec = spec

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        for obj in objects.values():
            assert isinstance(obj, (IngredientRun, MaterialRun, MeasurementRun, ProcessRun))
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
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.experiment.experiment_spec import ExperimentSpec
        assert isinstance(spec, ExperimentSpec)
        self._spec = spec

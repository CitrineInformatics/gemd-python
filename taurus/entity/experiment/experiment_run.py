from taurus.entity.experiment.base_experiment import BaseExperiment


class ExperimentRun(BaseExperiment):
    """An experiment run is a collection of Taurus run objects, with connections between them.
    """

    def __init__(self, objects, connections, uids, tags, spec):
        BaseExperiment.__init__(
            self, objects=objects, connections=connections, uids=uids, tags=tags
        )
        self._spec = None
        self.spec = spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.experiment.spec import ExperimentSpec
        assert isinstance(spec, ExperimentSpec)
        self._spec = spec

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        self._objects = objects  # TODO: check all objects are runs

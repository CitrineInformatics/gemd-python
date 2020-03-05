from taurus.entity.experiment.base_experiment import BaseExperiment


class ExperimentSpec(BaseExperiment):
    """An experiment spec is a collection of Taurus spec objects, with connections between them.
    """

    def __init__(self, objects, connections, uids, tags, template):
        BaseExperiment.__init__(
            self, objects=objects, connections=connections, uids=uids, tags=tags
        )
        self._template = None
        self.template = template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        from taurus.entity.experiment.template import ExperimentTemplate
        assert isinstance(template, ExperimentTemplate)
        self._template = template

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        self._objects = objects  # TODO: check all objects are specs

    def __call__(self):
        """Create a run state of this spec experiment."""
        from taurus.entity.experiment.run_experiment import ExperimentRun

        runs = dict()
        connections = list()

        return ExperimentRun(
            objects=runs,
            connections=connections,
            uids=self.uids,
            tags=self.tags,
            spec_experiment=self,
        )

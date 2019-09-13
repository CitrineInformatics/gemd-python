"""A process run, which turns into ingredients into a material."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_parameters import HasParameters


class ProcessRun(BaseObject, HasConditions, HasParameters):
    """
    Realization of a process.

    This includes links to the input materials and measured conditions and parameters
    ProcessRun includes a soft-link to the MaterialRun that it produces, if any
    """

    typ = "process_run"

    skip = {"_output_material", "_ingredients"}

    def __init__(self, name=None, spec=None,
                 conditions=None, parameters=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)

        self._ingredients = []

        self._spec = None
        self.spec = spec
        self._output_material = None

    @property
    def output_material(self):
        """Get the output material run."""
        return self._output_material

    @property
    def ingredients(self):
        """Get the input ingredient runs."""
        return self._ingredients

    @property
    def spec(self):
        """Get the process spec."""
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.object.process_spec import ProcessSpec
        from taurus.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (ProcessSpec, LinkByUID)):
            self._spec = spec
        else:
            raise ValueError("spec must be a ProcessSpec: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from taurus.entity.object.process_spec import ProcessSpec
        if isinstance(self.spec, ProcessSpec):
            return self.spec.template
        else:
            return None

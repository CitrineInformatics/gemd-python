"""A material run."""
from taurus.entity.object.base_object import BaseObject
from taurus.enumeration import SampleType


class MaterialRun(BaseObject):
    """Realization of a Material, with links to its spec, originating process, and measurements."""

    typ = "material_run"

    skip = {"_measurements"}

    def __init__(self, name=None, spec=None, process=None, sample_type="unknown",
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        self._process = None
        self._measurements = []
        self._sample_type = None
        self._spec = None

        self.spec = spec
        self.process = process
        self.sample_type = sample_type

    @property
    def process(self):
        """Get the originating process run."""
        return self._process

    @process.setter
    def process(self, process):
        from taurus.entity.object.process_run import ProcessRun
        from taurus.entity.link_by_uid import LinkByUID
        if process is None:
            self._process = None
        elif isinstance(process, LinkByUID):
            self._process = process
        elif isinstance(process, ProcessRun):
            process._output_material = self
            self._process = process
        else:
            raise ValueError("process must be a ProcessRun: {}".format(process))

    @property
    def measurements(self):
        """Get a list of measurement runs."""
        return self._measurements

    @property
    def sample_type(self):
        """Get the sample type."""
        return self._sample_type

    @sample_type.setter
    def sample_type(self, sample_type):
        self._sample_type = SampleType.get_value(sample_type)

    @property
    def spec(self):
        """Get the material spec."""
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.object.material_spec import MaterialSpec
        from taurus.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (MaterialSpec, LinkByUID)):
            self._spec = spec
        else:
            raise ValueError("spec must be a MaterialSpec: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from taurus.entity.object.material_spec import MaterialSpec
        if isinstance(self.spec, MaterialSpec):
            return self.spec.template
        else:
            return None

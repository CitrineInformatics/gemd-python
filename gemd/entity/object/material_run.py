from gemd.entity.object.base_object import BaseObject
from gemd.enumeration import SampleType


class MaterialRun(BaseObject):
    """
    A material run.

    This includes a link to the originating process and soft links to measurements.

    Parameters
    ----------
    name: str, required
        Name of the material run.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the material run.
    process: ProcessRun
        Process that produces this material.
    sample_type: str, optional
        The form of this sample. Optionals are "experimental", "virtual", "production", or
        "unknown." Default is "unknown."
    spec: MaterialSpec
        The material specification of which this is an instance.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    Attributes
    ----------
    measurements: List[MeasurementRun], optional
        Measurements performed on this material. The link is established by creating the
        measurement run and settings its `material` field to this material run.

    """

    typ = "material_run"

    skip = {"_measurements"}

    def __init__(self, name, *, spec=None, process=None, sample_type="unknown",
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
        from gemd.entity.object.process_run import ProcessRun
        from gemd.entity.link_by_uid import LinkByUID
        if self.process is not None and isinstance(self.process, ProcessRun):
            self.process._output_material = None
        if process is None:
            self._process = None
        elif isinstance(process, LinkByUID):
            self._process = process
        elif isinstance(process, ProcessRun):
            process._output_material = self
            self._process = process
        else:
            raise TypeError("process must be a ProcessRun or LinkByUID: {}".format(process))

    @property
    def measurements(self):
        """Get a list of measurement runs."""
        return self._measurements

    def _unset_measurement(self, meas):
        """Remove `meas` from this material's list of measurements."""
        if meas in self._measurements:
            self._measurements.remove(meas)

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
        from gemd.entity.object.material_spec import MaterialSpec
        from gemd.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (MaterialSpec, LinkByUID)):
            self._spec = spec
        else:
            raise TypeError("spec must be a MaterialSpec or LinkByUID: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from gemd.entity.object.material_spec import MaterialSpec
        if isinstance(self.spec, MaterialSpec):
            return self.spec.template
        else:
            return None

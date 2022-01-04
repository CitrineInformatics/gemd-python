from gemd.entity.object.material_spec import MaterialSpec
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_process import HasProcess
from gemd.entity.object.has_spec import HasSpec
from gemd.enumeration import SampleType
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list

from typing import Optional, Union, Iterable, List, Mapping, Type, Any


class MaterialRun(BaseObject, HasSpec, HasProcess):
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
    process: :class:`ProcessRun <gemd.entity.object.process_run.ProcessRun>`
        Process that produces this material.
    sample_type: str, optional
        The form of this sample. Optionals are "experimental", "virtual", "production", or
        "unknown." Default is "unknown."
    spec: :class:`MaterialSpec <gemd.entity.object.material_spec.MaterialSpec>`
        The material specification of which this is an instance.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    Attributes
    ----------
    measurements: List[:class:`MeasurementRun\
    <gemd.entity.object.measurement_run.MeasurementRun>`], optional
        Measurements performed on this material. The link is established by creating the
        measurement run and settings its `material` field to this material run.

    """

    typ = "material_run"

    skip = {"_measurements"}

    def __init__(self,
                 name: str,
                 *,
                 spec: Union[MaterialSpec, LinkByUID] = None,
                 process: Union[ProcessRun, LinkByUID] = None,
                 sample_type: Union[SampleType, str] = "unknown",
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
        from gemd.entity.object.measurement_run import MeasurementRun
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasSpec.__init__(self, spec=spec)
        self._process = None
        self._measurements = validate_list(None, [MeasurementRun, LinkByUID])
        self._sample_type = None

        self.process = process
        self.sample_type = sample_type

    @property
    def process(self) -> Union[ProcessRun, LinkByUID]:
        """Get the originating process run."""
        return self._process

    @process.setter
    def process(self, process: Union[ProcessRun, LinkByUID]):
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
    def measurements(self) -> List["MeasurementRun"]:
        """Get a read-only list of the measurement runs."""
        return self._measurements

    @property
    def sample_type(self) -> str:
        """Get the sample type."""
        return self._sample_type

    @sample_type.setter
    def sample_type(self, sample_type: Union[SampleType, str]):
        self._sample_type = SampleType.get_value(sample_type)

    @staticmethod
    def _spec_type() -> Type:
        """Required method to satisfy HasTemplates mix-in."""
        return MaterialSpec

    def _dict_for_compare(self) -> Mapping[str, Any]:
        """Support for recursive equals."""
        base = super()._dict_for_compare()
        base['measurements'] = self.measurements
        return base

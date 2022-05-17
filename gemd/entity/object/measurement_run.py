from gemd.entity.object.measurement_spec import MeasurementSpec
from gemd.entity.object.material_run import MaterialRun
from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_material import HasMaterial
from gemd.entity.object.has_spec import HasSpec
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_properties import HasProperties
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_source import HasSource
from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.attribute.property import Property
from gemd.entity.source.performed_source import PerformedSource
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID

from typing import Optional, Union, Iterable, Mapping, Type


class MeasurementRun(BaseObject, HasMaterial, HasSpec, HasConditions, HasProperties,
                     HasParameters, HasSource):
    """
    A measurement run.

    This contains a link to the material the measurement is performed on, as well as links to
    any properties, conditions, and parameters.

    Parameters
    ----------
    name: str, required
        Name of the measurement run.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the measurement run.
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`], optional
        Conditions under which this measurement run occurs.
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`], optional
        Parameters of this measurement run.
    properties: List[:class:`Property <gemd.entity.attribute.property.Property>`], optional
        Properties that are measured during this measurement run.
    spec: :class:`MeasurementSpec <gemd.entity.object.measurement_spec.MeasurementSpec>`
        The measurement specification of which this is an instance.
    material: :class:`MaterialRun <gemd.entity.object.material_run.MaterialRun>`
        The material run being measured.
    spec: :class:`MaterialSpec <gemd.entity.object.material_spec.MaterialSpec>`
        The material specification of which this is an instance.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.
    source: :class:`PerformedSource\
    <gemd.entity.source.performed_source.PerformedSource>`, optional
        Information about the person who performed the run and when.

    """

    typ = "measurement_run"

    def __init__(self,
                 name: str,
                 *,
                 spec: Union[MeasurementSpec, LinkByUID] = None,
                 material: Union[MaterialRun, LinkByUID] = None,
                 properties: Union[Property, Iterable[Property]] = None,
                 conditions: Union[Condition, Iterable[Condition]] = None,
                 parameters: Union[Parameter, Iterable[Parameter]] = None,
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None,
                 source: PerformedSource = None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasSpec.__init__(self, spec=spec)
        HasProperties.__init__(self, properties)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)
        HasSource.__init__(self, source)

        self._material = None
        self.material = material

    @property
    def material(self) -> Union[MaterialRun, LinkByUID]:
        """Get the material."""
        return self._material

    @material.setter
    def material(self, value: Union[MaterialRun, LinkByUID]):
        if isinstance(self._material, MaterialRun):
            # This could throw an exception if it's not in the list, but then something else broke
            self._material.measurements.remove(self)

        if value is None or isinstance(value, (MaterialRun, LinkByUID)):
            self._material = value
            if isinstance(value, MaterialRun):
                value.measurements.append(self)
        else:
            raise TypeError("material must be a MaterialRun or LinkByUID: {}".format(value))

    @staticmethod
    def _spec_type() -> Type:
        """Required method to satisfy HasTemplates mix-in."""
        return MeasurementSpec

from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_properties import HasProperties
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_source import HasSource
from gemd.entity.setters import validate_list
from gemd.entity.valid_list import ValidList


class MeasurementRun(BaseObject, HasConditions, HasProperties, HasParameters, HasSource):
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
    conditions: List[Condition], optional
        Conditions under which this measurement run occurs.
    parameters: List[Parameter], optional
        Parameters of this measurement run.
    properties: List[Property], optional
        Properties that are measured during this measurement run.
    spec: MeasurementSpec
        The measurement specification of which this is an instance.
    material: MaterialRun
        The material run being measured.
    spec: MaterialSpec
        The material specification of which this is an instance.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.
    source: PerformedSource, optional
        Information about the person who performed the run and when.

    """

    typ = "measurement_run"

    def __init__(self, name, *, spec=None, material=None,
                 properties=None, conditions=None, parameters=None,
                 uids=None, tags=None, notes=None, file_links=None, source=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasProperties.__init__(self, properties)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)
        HasSource.__init__(self, source)

        self._material = None
        self.material = material
        self._spec = None
        self.spec = spec

    @property
    def material(self):
        """Get the material."""
        return self._material

    @material.setter
    def material(self, value):
        from gemd.entity.object import MaterialRun
        from gemd.entity.link_by_uid import LinkByUID
        if self._material is not None and isinstance(self._material, MaterialRun):
            self._material._unset_measurement(self)
        if value is None:
            self._material = value
        elif isinstance(value, MaterialRun):
            self._material = value
            if not isinstance(value.measurements, ValidList):
                value._measurements = validate_list(self, [MeasurementRun, LinkByUID])
            else:
                value._measurements.append(self)
        elif isinstance(value, LinkByUID):
            self._material = value
        else:
            raise TypeError("material must be a MaterialRun or LinkByUID: {}".format(value))

    @property
    def spec(self):
        """Get the measurement spec."""
        return self._spec

    @spec.setter
    def spec(self, spec):
        from gemd.entity.object.measurement_spec import MeasurementSpec
        from gemd.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (MeasurementSpec, LinkByUID)):
            self._spec = spec
        else:
            raise TypeError("spec must be a MeasurementSpec or LinkByUID: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from gemd.entity.object.measurement_spec import MeasurementSpec
        if isinstance(self.spec, MeasurementSpec):
            return self.spec.template
        else:
            return None

"""A measurement run performed on a material."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_properties import HasProperties
from taurus.entity.object.has_parameters import HasParameters
from taurus.entity.setters import validate_list
from taurus.entity.valid_list import ValidList


class MeasurementRun(BaseObject, HasConditions, HasProperties, HasParameters):
    """
    Realization of a measurement, which includes measured conditions, properties, and parameters.

    MeasurementRun includes a soft-link to the MaterialRun that contains it, if any.
    """

    typ = "measurement_run"

    def __init__(self, name=None, spec=None, material=None,
                 properties=None, conditions=None, parameters=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasProperties.__init__(self, properties)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)

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
        from taurus.entity.object import MaterialRun
        from taurus.entity.link_by_uid import LinkByUID
        if value is None:
            self._material = value
        elif isinstance(value, MaterialRun):
            self._material = value
            if not isinstance(value.measurements, ValidList):
                value._measurements = validate_list(self, MeasurementRun)
            else:
                value._measurements.append(self)
        elif isinstance(value, LinkByUID):
            self._material = value
        else:
            raise ValueError("material must be a MaterialRun or LinkByUID: {}".format(value))

    @property
    def spec(self):
        """Get the measurement spec."""
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.object.measurement_spec import MeasurementSpec
        from taurus.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (MeasurementSpec, LinkByUID)):
            self._spec = spec
        else:
            raise ValueError("spec must be a MeasurementSpec: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from taurus.entity.object.measurement_spec import MeasurementSpec
        if isinstance(self.spec, MeasurementSpec):
            return self.spec.template
        else:
            return None

"""A measurement spec."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_parameters import HasParameters
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_template import HasTemplate


class MeasurementSpec(BaseObject, HasParameters, HasConditions, HasTemplate):
    """Specification of a measurement, including the relevant conditions and parameters."""

    typ = "measurement_spec"

    def __init__(self, name=None, template=None,
                 parameters=None, conditions=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, uids=uids, tags=tags, notes=notes, file_links=file_links)
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)
        self.name = name
        HasTemplate.__init__(self, template=template)

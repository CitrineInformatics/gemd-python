from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_template import HasTemplate


class MeasurementSpec(BaseObject, HasParameters, HasConditions, HasTemplate):
    """
    A measurement specification.

    This includes links to the conditions and parameters under which the measurement is
    expected to be performed.

    Parameters
    ----------
    name: str, required
        Name of the measurement spec.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the measurement spec.
    conditions: List[Condition], optional
        Conditions under which this measurement spec occurs.
    parameters: List[Parameter], optional
        Parameters of this measurement spec.
    template: MeasurementTemplate
        A template bounding the valid values for the measurement's properties, parameters,
        and conditions.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "measurement_spec"

    def __init__(self, name, *, template=None,
                 parameters=None, conditions=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)
        HasTemplate.__init__(self, template=template)

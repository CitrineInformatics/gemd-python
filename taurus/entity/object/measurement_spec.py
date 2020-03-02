import copy

from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.has_parameters import HasParameters
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_template import HasTemplate


class MeasurementSpec(BaseObject, HasParameters, HasConditions, HasTemplate):
    """
    A measurement specification.

    This includes links to the conditions and parameters under which the measurement is
    expected to be performed.

    Parameters
    ----------
    name: str, optional
        Name of the measurement spec.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
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

    def __init__(
        self,
        name=None,
        template=None,
        parameters=None,
        conditions=None,
        uids=None,
        tags=None,
        notes=None,
        file_links=None,
    ):
        BaseObject.__init__(
            self, name=name, uids=uids, tags=tags, notes=notes, file_links=file_links
        )
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)
        HasTemplate.__init__(self, template=template)

    def __call__(
        self,
        name=None,
        spec=None,
        material=None,
        properties=None,
        conditions=None,
        parameters=None,
        uids=None,
        tags=None,
        notes=None,
        file_links=None,
        source=None,
    ):
        """Produces a measurement run that is linked to this measurement spec."""

        if not name:  # set defaults if no constructor values were supplied
            name = self.name
        if not spec:
            spec = self
        if not parameters:  # inherit the parameters from the spec
            parameters = [copy.copy(param) for param in self.parameters]
        if not conditions:  # inherit the conditions from the spec
            conditions = [copy.copy(cond) for cond in self.conditions]
        if not tags:
            tags = self.tags

        return MeasurementRun(
            name=name,
            spec=spec,
            material=material,
            properties=properties,
            conditions=conditions,
            parameters=parameters,
            uids=uids,
            tags=tags,
            notes=notes,
            file_links=file_links,
            source=source,
        )

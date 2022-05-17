from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.template.measurement_template import MeasurementTemplate
from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID

from typing import Optional, Union, Iterable, Mapping, Type


class MeasurementSpec(BaseObject, HasTemplate, HasParameters, HasConditions):
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
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`], optional
        Conditions under which this measurement spec occurs.
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`], optional
        Parameters of this measurement spec.
    template: :class:`MeasurementTemplate\
    <gemd.entity.object.measurement_template.MeasurementTemplate>`
        A template bounding the valid values for the measurement's properties, parameters,
        and conditions.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "measurement_spec"

    def __init__(self,
                 name: str,
                 *,
                 template: Optional[Union[MeasurementTemplate, LinkByUID]] = None,
                 conditions: Union[Condition, Iterable[Condition]] = None,
                 parameters: Union[Parameter, Iterable[Parameter]] = None,
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasTemplate.__init__(self, template=template)
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)

    @staticmethod
    def _template_type() -> Type:
        """Communicate expected template type to parent class."""
        return MeasurementTemplate

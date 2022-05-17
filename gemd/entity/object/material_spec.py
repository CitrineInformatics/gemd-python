from gemd.entity.attribute.property_and_conditions import PropertyAndConditions
from gemd.entity.object.process_spec import ProcessSpec
from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_process import HasProcess
from gemd.entity.object.has_properties import HasProperties
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.template.has_property_templates import HasPropertyTemplates
from gemd.entity.template.material_template import MaterialTemplate
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list

from typing import Optional, Union, Iterable, List, Set, Mapping, Type


class MaterialSpec(BaseObject, HasTemplate, HasProcess, HasProperties):
    """
    A material specification.

    This includes a link to the originating process and specified properties with conditions.

    Parameters
    ----------
    name: str, required
        Name of the material spec.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the material spec.
    process: :class:`ProcessSpec <gemd.entity.object.process_spec.ProcessSpec>`
        Process that produces this material.
    properties: List[:class:`PropertyAndConditions\
    <gemd.entity.attribute.property_and_conditions.PropertyAndConditions>`], optional
        Properties of the material, along with an optional list of conditions under which
        those properties are measured.
    template: :class:`MaterialTemplate\
    <gemd.entity.template.material_template.MaterialTemplate>`, optional
        A template bounding the valid values for this material's properties.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "material_spec"

    def __init__(self,
                 name: str,
                 *,
                 template: Optional[Union[MaterialTemplate, LinkByUID]] = None,
                 process: Union[ProcessSpec, LinkByUID] = None,
                 properties: Union[Iterable[PropertyAndConditions], PropertyAndConditions] = None,
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasTemplate.__init__(self, template)
        self._properties = None
        self.properties = properties
        self._process = None
        self.process = process

    @property
    def properties(self) -> List[PropertyAndConditions]:
        """Get the list of property-and-conditions."""
        return self._properties

    @properties.setter
    def properties(self,
                   properties: Union[Iterable[PropertyAndConditions], PropertyAndConditions]):
        """Set the list of property-and-conditions."""
        checker = self._generate_template_check(HasPropertyTemplates.validate_property)
        self._properties = validate_list(properties, PropertyAndConditions, trigger=checker)

    @property
    def process(self) -> Union[ProcessSpec, LinkByUID]:
        """Get the originating process spec."""
        return self._process

    @process.setter
    def process(self, process: Union[ProcessSpec, LinkByUID]):
        """
        Link to the ProcessSpec that creates this MaterialSpec.

        If the input, process, is not an instance of ProcessSpec, raise an error.
        Otherwise, make a bidirectional link: this MaterialSpec is linked to
        process, and process has its output_material field linked to this MaterialSpec
        """
        from gemd.entity.object.process_spec import ProcessSpec
        from gemd.entity.link_by_uid import LinkByUID
        if self.process is not None and isinstance(self.process, ProcessSpec):
            self.process._output_material = None
        if process is None:
            self._process = None
        elif isinstance(process, LinkByUID):
            self._process = process
        elif isinstance(process, ProcessSpec):
            process._output_material = self
            self._process = process
        else:
            raise TypeError(f"process must be an instance of ProcessSpec or LinkByUID; "
                            f"instead received type {type(process)}: {process}")

    @staticmethod
    def _template_type() -> Type:
        """Communicate expected template type to parent class."""
        return MaterialTemplate

    def _local_dependencies(self) -> Set[Union["BaseEntity", "LinkByUID"]]:
        """Return a set of all immediate dependencies (no recursion)."""
        result = set()
        for attr in self.properties:
            if attr.property.template is not None:
                result.add(attr.property.template)
            for condition in attr.conditions:
                if condition.template is not None:
                    result.add(condition.template)
        return result

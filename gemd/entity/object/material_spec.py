from gemd.entity.attribute.property_and_conditions import PropertyAndConditions
from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.setters import validate_list


class MaterialSpec(BaseObject, HasTemplate):
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
    process: ProcessSpec
        Process that produces this material.
    properties: List[PropertyAndConditions], optional
        Properties of the material, along with an optional list of conditions under which
        those properties are measured.
    template: MaterialTemplate, optional
        A template bounding the valid values for this material's properties.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "material_spec"

    def __init__(self, name, *, template=None,
                 properties=None, process=None, uids=None, tags=None,
                 notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        self._properties = None
        self.properties = properties
        self._process = None
        self.process = process
        HasTemplate.__init__(self, template)

    @property
    def properties(self):
        """Get the list of property-and-conditions."""
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = validate_list(properties, PropertyAndConditions)

    @property
    def process(self):
        """Get the originating process spec."""
        return self._process

    @process.setter
    def process(self, process):
        """
        Link to the ProcessSpec that creates this MaterialSpec.

        If the input, process, is not an instance of ProcessSpec, raise an error.
        Otherwise, make a bi-directional link: this MaterialSpec is linked to
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
            raise TypeError("process must be an instance of ProcessSpec or LinkByUID; "
                            "instead received type {}: {}".format(type(process), process))

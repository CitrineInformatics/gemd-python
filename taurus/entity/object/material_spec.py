"""A material spec."""
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_template import HasTemplate
from taurus.entity.setters import validate_list


class MaterialSpec(BaseObject, HasTemplate):
    """
    Specification of the intent of a material.

    This includes links to originating process and specified properties
    """

    typ = "material_spec"

    def __init__(self, name=None, template=None,
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
        from taurus.entity.object.process_spec import ProcessSpec
        from taurus.entity.link_by_uid import LinkByUID
        if process is None:
            self._process = None
        elif isinstance(process, LinkByUID):
            self._process = process
        elif isinstance(process, ProcessSpec):
            process._output_material = self
            self._process = process
        else:
            raise ValueError("process must be an instance of ProcessSpec; "
                             "instead received type {}: {}".format(type(process), process))

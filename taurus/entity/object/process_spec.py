"""A process spec, the intent of a process that converts ingredients into an intended material."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_parameters import HasParameters
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_template import HasTemplate


class ProcessSpec(BaseObject, HasParameters, HasConditions, HasTemplate):
    """
    Specification of a process.

    This includes a link to the input material specs and relevant conditions and parameters
    ProcessSpec includes a soft-link to the MaterialSpec that it produces, if any
    """

    typ = "process_spec"

    skip = {"_output_material", "_ingredients"}

    def __init__(self, name=None, template=None,
                 parameters=None, conditions=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)

        self._ingredients = []

        # By default, a ProcessSpec is not linked to any MaterialSpec.
        # If a MaterialSpec is linked to this ProcessSpec,
        # then the field self._output_material will be automatically populated
        self._output_material = None

        HasTemplate.__init__(self, template=template)

    @property
    def ingredients(self):
        """Get the list of input ingredient specs."""
        return self._ingredients

    @property
    def output_material(self):
        """Get the output material spec."""
        return self._output_material

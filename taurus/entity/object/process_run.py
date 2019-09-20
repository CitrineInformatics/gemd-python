from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_parameters import HasParameters


class ProcessRun(BaseObject, HasConditions, HasParameters):
    """
    A process run.

    Processes transform zero or more input materials into exactly one output material.
    This includes links to conditions and parameters under which the process was performed,
    as well as soft links to the output material and each of the input ingredients.

    Parameters
    ----------
    name: str, optional
        Name of the process run.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the process run.
    conditions: List[Condition], optional
        Conditions under which this process run occurs.
    parameters: List[Parameter], optional
        Parameters of this process run.
    spec: ProcessSpec
        Spec for this process run.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    Attributes
    ----------
    output_material: MaterialRun
        The material run that this process run produces. The link is established by creating
        the material run and settings its `process` field to this process run.

    ingredients: List[IngredientRun]
        Ingredient runs that act as inputs to this process run. The link is established by
        creating each ingredient run and setting its `process` field to this process run.

    """

    typ = "process_run"

    skip = {"_output_material", "_ingredients"}

    def __init__(self, name=None, spec=None,
                 conditions=None, parameters=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)

        self._ingredients = []

        self._spec = None
        self.spec = spec
        self._output_material = None

    @property
    def output_material(self):
        """Get the output material run."""
        return self._output_material

    @property
    def ingredients(self):
        """Get the input ingredient runs."""
        return self._ingredients

    @property
    def spec(self):
        """Get the process spec."""
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.object.process_spec import ProcessSpec
        from taurus.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (ProcessSpec, LinkByUID)):
            self._spec = spec
        else:
            raise ValueError("spec must be a ProcessSpec: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from taurus.entity.object.process_spec import ProcessSpec
        if isinstance(self.spec, ProcessSpec):
            return self.spec.template
        else:
            return None

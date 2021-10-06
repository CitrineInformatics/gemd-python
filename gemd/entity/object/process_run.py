from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_source import HasSource
from gemd.entity.setters import validate_list


class ProcessRun(BaseObject, HasConditions, HasParameters, HasSource):
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
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the process run.
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`], optional
        Conditions under which this process run occurs.
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`], optional
        Parameters of this process run.
    spec: :class:`ProcessSpec <gemd.entity.object.process_spec.ProcessSpec>`
        Spec for this process run.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.
    source: :class:`PerformedSource\
    <gemd.entity.source.performed_source.PerformedSource>`, optional
        Information about the person who performed the run and when.

    Attributes
    ----------
    output_material: :class:`MaterialRun <gemd.entity.object.material_run.MaterialRun>`
        The material run that this process run produces. The link is established by creating
        the material run and settings its `process` field to this process run.

    ingredients: List[:class:`IngredientRun <gemd.entity.object.ingredient_run.IngredientRun>`]
        Ingredient runs that act as inputs to this process run. The link is established by
        creating each ingredient run and setting its `process` field to this process run.

    """

    typ = "process_run"

    skip = {"_output_material", "_ingredients", "_active_comparison"}

    def __init__(self, name, *, spec=None,
                 conditions=None, parameters=None,
                 uids=None, tags=None, notes=None, file_links=None, source=None):
        from gemd.entity.object.ingredient_run import IngredientRun
        from gemd.entity.link_by_uid import LinkByUID

        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)
        HasSource.__init__(self, source)

        self._spec = None
        self.spec = spec
        self._output_material = None
        self._ingredients = validate_list(None, [IngredientRun, LinkByUID])
        self._active_comparison = set()

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
        from gemd.entity.object.process_spec import ProcessSpec
        from gemd.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (ProcessSpec, LinkByUID)):
            self._spec = spec
        else:
            raise TypeError("spec must be a ProcessSpec or LinkByUID: {}".format(spec))

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from gemd.entity.object.process_spec import ProcessSpec
        if isinstance(self.spec, ProcessSpec):
            return self.spec.template
        else:
            return None

    def __eq__(self, other):
        # To avoid infinite recursion, fast return on revisit; vulnerable to exceptions
        if other in self._active_comparison:  # Cycle encountered
            return True  # This will functionally be & with the correct result of ==

        self._active_comparison.add(other)
        try:
            result = super().__eq__(other)

            # Equals needs to crawl into ingredients
            if result is True and isinstance(other, ProcessRun):
                if len(self.ingredients) == len(other.ingredients):
                    result = all(ing in other.ingredients for ing in self.ingredients)
                elif (len(self.ingredients) == 0 and len(self.uids) != 0) \
                        or (len(other.ingredients) == 0 and len(other.uids) != 0):
                    result = True  # One can be empty if you flattened
                else:
                    result = False
        finally:
            self._active_comparison.remove(other)

        return result

    # Note the hash function checks if objects are identical, as opposed to the equals method,
    # which checks if fields are equal.  This is because BaseEntities are fundamentally
    # mutable objects.  Note that if you define an __eq__ method without defining a __hash__
    # method, the object will become unhashable.
    # https://docs.python.org/3/reference/datamodel.html#object.__hash
    def __hash__(self):
        return super().__hash__()

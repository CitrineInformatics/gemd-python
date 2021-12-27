from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_spec import HasSpec
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_source import HasSource
from gemd.entity.attribute import Condition, Parameter
from gemd.entity.source.performed_source import PerformedSource
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.file_link import FileLink
from gemd.entity.setters import validate_list

from typing import Union, Optional, Type, Collection, Mapping


class ProcessRun(BaseObject, HasSpec, HasConditions, HasParameters, HasSource):
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

    skip = {"_output_material", "_ingredients"}

    def __init__(self, name: str, *,
                 spec: Union[BaseObject, LinkByUID, None] = None,
                 conditions: Optional[Condition] = None,
                 parameters: Optional[Parameter] = None,
                 uids: Optional[Mapping[str, str]] = None,
                 tags: Union[Collection[str], str, None] = None,
                 notes: Optional[str] = None,
                 file_links: Optional[Collection[FileLink]] = None,
                 source: Optional[PerformedSource] = None
                 ):
        from gemd.entity.object.ingredient_run import IngredientRun
        from gemd.entity.link_by_uid import LinkByUID

        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasSpec.__init__(self, spec)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)
        HasSource.__init__(self, source)

        self._ingredients = []
        self._spec = None
        self.spec = spec
        self._output_material = None
        self._ingredients = validate_list(None, [IngredientRun, LinkByUID])

    @property
    def output_material(self):
        """Get the output material run."""
        return self._output_material

    @property
    def ingredients(self):
        """Get the input ingredient runs."""
        return self._ingredients

    @staticmethod
    def _spec_type() -> Type:
        """Get the expected type of spec for this object (property of child)."""
        from gemd.entity.object import ProcessSpec
        return ProcessSpec

    @property
    def template(self):
        """Get the template of the spec, if applicable."""
        from gemd.entity.object.process_spec import ProcessSpec
        if isinstance(self.spec, ProcessSpec):
            return self.spec.template
        else:
            return None

    def _dict_for_compare(self):
        """Support for recursive equals."""
        base = super()._dict_for_compare()
        base['ingredients'] = self.ingredients
        return base

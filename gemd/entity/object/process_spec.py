from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_parameters import HasParameters
from gemd.entity.object.has_conditions import HasConditions
from gemd.entity.object.has_template import HasTemplate
from gemd.entity.template.process_template import ProcessTemplate
from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list

from typing import Optional, Union, Iterable, List, Mapping, Dict, Type, Any


class ProcessSpec(BaseObject, HasTemplate, HasParameters, HasConditions):
    """
    A process specification.

    Processes transform zero or more input materials into exactly one output material.
    This includes links to the parameters and conditions under which the process is expected
    to be performed, as well as soft links to the output material and the input ingredients.

    Parameters
    ----------
    name: str, required
        Name of the process spec.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the process spec.
    conditions: List[:class:`Condition <gemd.entity.attribute.condition.Condition>`], optional
        Conditions under which this process spec occurs.
    parameters: List[:class:`Parameter <gemd.entity.attribute.parameter.Parameter>`], optional
        Parameters of this process spec.
    template: :class:`ProcessTemplate\
    <gemd.entity.template.process_template.ProcessTemplate>`, optional
        A template bounding the valid values for this process's parameters and conditions.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    Attributes
    ----------
    output_material: :class:`MaterialSpec <gemd.entity.object.material_spec.MaterialSpec>`
        The material spec that this process spec produces. The link is established by creating
        the material spec and settings its `process` field to this process spec.

    ingredients: List[:class:`IngredientSpec\
    <gemd.entity.object.ingredient_spec.IngredientSpec>`], optional
        Ingredient specs that act as inputs to this process spec. The link is established by
        creating each ingredient spec and setting its `process` field to this process spec.

    """

    typ = "process_spec"

    skip = {"_output_material", "_ingredients"}

    def __init__(self,
                 name: str,
                 *,
                 template: Optional[Union[ProcessTemplate, LinkByUID]] = None,
                 conditions: Union[Condition, Iterable[Condition]] = None,
                 parameters: Union[Parameter, Iterable[Parameter]] = None,
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
        from gemd.entity.object.ingredient_spec import IngredientSpec
        from gemd.entity.link_by_uid import LinkByUID

        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasTemplate.__init__(self, template=template)
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)

        # By default, a ProcessSpec is not linked to any MaterialSpec.
        # If a MaterialSpec is linked to this ProcessSpec,
        # then the field self._output_material will be automatically populated
        self._output_material = None
        self._ingredients = validate_list(None, [IngredientSpec, LinkByUID])

    @staticmethod
    def _template_type() -> Type:
        """Communicate expected template type to parent class."""
        return ProcessTemplate

    @property
    def ingredients(self) -> List["IngredientSpec"]:
        """Get the list of input ingredient specs."""
        return self._ingredients

    @property
    def output_material(self) -> Optional["MaterialSpec"]:  # noqa: F821
        """Get the output material spec."""
        return self._output_material

    def _dict_for_compare(self) -> Dict[str, Any]:
        """Support for recursive equals."""
        base = super()._dict_for_compare()
        base['ingredients'] = self.ingredients
        return base

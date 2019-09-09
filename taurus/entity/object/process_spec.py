"""A process spec, the intent of a process that converts ingredients into an intended material."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_parameters import HasParameters
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_template import HasTemplate
from taurus.entity.setters import validate_list


class ProcessSpec(BaseObject, HasParameters, HasConditions, HasTemplate):
    """
    Specification of a process.

    This includes a link to the input material specs and relevant conditions and parameters
    ProcessSpec includes a soft-link to the MaterialSpec that it produces, if any
    """

    typ = "process_spec"

    skip = {"_output_material"}

    def __init__(self, name=None, ingredients=None, template=None,
                 parameters=None, conditions=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, uids=uids, tags=tags, notes=notes, file_links=file_links)
        HasParameters.__init__(self, parameters=parameters)
        HasConditions.__init__(self, conditions=conditions)
        self.name = name

        self._ingredients = None
        self.ingredients = ingredients

        # By default, a ProcessSpec is not linked to any MaterialSpec.
        # If a MaterialSpec is linked to this ProcessSpec,
        # then the field self._output_material will be automatically populated
        self._output_material = None

        HasTemplate.__init__(self, template=template)

    @property
    def ingredients(self):
        """Get the list of input ingredient specs."""
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        from taurus.entity.object.ingredient_spec import IngredientSpec
        from taurus.entity.link_by_uid import LinkByUID
        self._ingredients = validate_list(ingredients, [IngredientSpec, LinkByUID])
        ingredient_names = [x.unique_label for x in self._ingredients
                            if isinstance(x, IngredientSpec) and x.unique_label is not None]
        if len(ingredient_names) > len(set(ingredient_names)):
            raise ValueError("Two ingredients were assigned the same name")

    @property
    def output_material(self):
        """Get the output material spec."""
        return self._output_material

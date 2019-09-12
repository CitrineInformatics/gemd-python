"""A process run, which turns into ingredients into a material."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_conditions import HasConditions
from taurus.entity.object.has_parameters import HasParameters
from taurus.entity.setters import validate_list


class ProcessRun(BaseObject, HasConditions, HasParameters):
    """
    Realization of a process.

    This includes links to the input materials and measured conditions and parameters
    ProcessRun includes a soft-link to the MaterialRun that it produces, if any
    """

    typ = "process_run"

    skip = {"_output_material"}

    def __init__(self, name=None, spec=None, ingredients=None,
                 conditions=None, parameters=None,
                 uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags, notes=notes,
                            file_links=file_links)
        HasConditions.__init__(self, conditions)
        HasParameters.__init__(self, parameters)

        self._ingredients = None
        self.ingredients = ingredients

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

    @ingredients.setter
    def ingredients(self, ingredients):
        from taurus.entity.object.ingredient_run import IngredientRun
        from taurus.entity.link_by_uid import LinkByUID
        self._ingredients = validate_list(ingredients, [IngredientRun, LinkByUID])
        ingredient_names = [x.name for x in self._ingredients
                        if isinstance(x, IngredientRun) and x.name is not None]
        if len(ingredient_names) > len(set(ingredient_names)):
            raise ValueError("Two ingredients were assigned the same name")

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

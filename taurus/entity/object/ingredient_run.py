"""An ingredient run is a material run being used in a process run.."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_quantities import HasQuantities
from taurus.entity.setters import validate_list
from taurus.entity.valid_list import ValidList


class IngredientRun(BaseObject, HasQuantities):
    """An ingredient run, with quantities and link to originating material."""

    typ = "ingredient_run"

    def __init__(self, material=None, process=None, name=None, labels=None,
                 mass_fraction=None, volume_fraction=None, number_fraction=None,
                 absolute_quantity=None,
                 spec=None, uids=None, tags=None, notes=None, file_links=None):
        """
        Create an IngredientRun object.

        Assigns quantities and labels to a material being used in a process
        :param material: MaterialRun that is being used as the ingredient
        :param name: of the ingredient as used in the process, e.g. "the peanut butter"
        :param labels: that this ingredient belongs to, e.g. "spread" or "solvent"
        :param mass_fraction: fraction of the ingredients that is this input ingredient, by mass
        :param volume_fraction: fraction of the ingredients that is this ingredient, by volume
        :param number_fraction: fraction of the ingredients that is this ingredient, by number
        :param absolute_quantity: quantity of this ingredient in an absolute sense, e.g. 2 cups
        """
        BaseObject.__init__(self, name, uids, tags, notes=notes, file_links=file_links)
        HasQuantities.__init__(self, mass_fraction, volume_fraction, number_fraction,
                               absolute_quantity)

        self._material = None
        self._process = None
        self._spec = None
        self._labels = None

        self.material = material
        self.process = process
        self.spec = spec
        self.labels = labels

    @property
    def labels(self):
        """Get labels."""
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = validate_list(labels, str)

    @property
    def material(self):
        """Get the material."""
        return self._material

    @material.setter
    def material(self, material):
        from taurus.entity.object import MaterialRun
        from taurus.entity.link_by_uid import LinkByUID
        if material is None:
            self._material = None
        elif isinstance(material, (MaterialRun, LinkByUID)):
            self._material = material
        else:
            raise ValueError("IngredientRun.material must be a MaterialRun")

    @property
    def process(self):
        """Get the material."""
        return self._process

    @process.setter
    def process(self, process):
        from taurus.entity.object import ProcessRun
        from taurus.entity.link_by_uid import LinkByUID
        if process is None:
            self._process = None
        elif isinstance(process, ProcessRun):
            self._process = process
            if not isinstance(process.ingredients, ValidList):
                process._ingredients = validate_list(self, IngredientRun)
            else:
                process._ingredients.append(self)
        elif isinstance(process, LinkByUID):
            self._process = process
        else:
            raise ValueError("IngredientRun.process must be a ProcessRun")

    @property
    def spec(self):
        """Get the ingredient spec."""
        return self._spec

    @spec.setter
    def spec(self, spec):
        from taurus.entity.object.ingredient_spec import IngredientSpec
        from taurus.entity.link_by_uid import LinkByUID
        if spec is None:
            self._spec = None
        elif isinstance(spec, (IngredientSpec, LinkByUID)):
            self._spec = spec
        else:
            raise ValueError("spec must be a IngredientSpec: {}".format(spec))

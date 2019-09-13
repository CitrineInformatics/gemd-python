"""An ingredient spec is the intent of a material being used in a process."""
from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_quantities import HasQuantities
from taurus.entity.setters import validate_list
from taurus.entity.valid_list import ValidList


class IngredientSpec(BaseObject, HasQuantities):
    """Ingredient spec, with quantities and links to originating material."""

    typ = "ingredient_spec"

    def __init__(self, material=None, process=None, name=None, labels=None,
                 mass_fraction=None, volume_fraction=None, number_fraction=None,
                 absolute_quantity=None,
                 uids=None, tags=None, notes=None, file_links=None):
        """
        Create an IngredientSpec object.

        Assigns a unique_label and other descriptive labels to a material used as an ingredient
        :param material: MaterialSpec that is being used as the ingredient
        :param process: ProcessSpec that uses this ingredient
        :param name: of the ingredient as used in the process, i.e. "the peanut butter"
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
        self._labels = None

        self.material = material
        self.process = process
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
        """Get the material spec."""
        return self._material

    @material.setter
    def material(self, material):
        from taurus.entity.object.material_spec import MaterialSpec
        from taurus.entity.link_by_uid import LinkByUID
        if material is None:
            self._material = None
        elif isinstance(material, (MaterialSpec, LinkByUID)):
            self._material = material
        else:
            raise ValueError("IngredientSpec.material must be a MaterialSpec")

    @property
    def process(self):
        """Get the material."""
        return self._process

    @process.setter
    def process(self, process):
        from taurus.entity.object import ProcessSpec
        from taurus.entity.link_by_uid import LinkByUID
        if process is None:
            self._process = None
        elif isinstance(process, ProcessSpec):
            self._process = process
            if not isinstance(process.ingredients, ValidList):
                process._ingredients = validate_list(self, IngredientSpec)
            else:
                process._ingredients.append(self)
        elif isinstance(process, LinkByUID):
            self._process = process
        else:
            raise ValueError("IngredientSpec.process must be a ProcessSpec")

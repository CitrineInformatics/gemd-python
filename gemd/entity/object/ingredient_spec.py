from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_quantities import HasQuantities
from gemd.entity.setters import validate_list
from gemd.entity.valid_list import ValidList


class IngredientSpec(BaseObject, HasQuantities):
    """
    An ingredient specification.

    Ingredients annotate a material with information about its usage in a process.

    Parameters
    ----------
    name: str, required
        Label on the ingredient that is unique within the process that contains it.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the ingredient spec.
    material: MaterialSpec
        Material that this ingredient is.
    process: ProcessSpec
        Process that this ingredient is used in.
    mass_fraction: :py:class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The mass fraction of the ingredient in the process.
    volume_fraction: :py:class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The volume fraction of the ingredient in the process.
    number_fraction: :py:class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The number fraction of the ingredient in the process.
    absolute_quantity: :py:class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The absolute quantity of the ingredient in the process.
    labels: List[str], optional
        Additional labels on the ingredient that must be unique.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "ingredient_spec"

    def __init__(self, name, *, material=None, process=None, labels=None,
                 mass_fraction=None, volume_fraction=None, number_fraction=None,
                 absolute_quantity=None,
                 uids=None, tags=None, notes=None, file_links=None):
        """
        Create an IngredientSpec object.

        Assigns a unique_label and other descriptive labels to a material used as an ingredient
        :param name: of the ingredient as used in the process, i.e. "the peanut butter"
        :param material: MaterialSpec that is being used as the ingredient
        :param process: ProcessSpec that uses this ingredient
        :param labels: that this ingredient belongs to, e.g. "spread" or "solvent"
        :param mass_fraction: fraction of the ingredients that is this input ingredient, by mass
        :param volume_fraction: fraction of the ingredients that is this ingredient, by volume
        :param number_fraction: fraction of the ingredients that is this ingredient, by number
        :param absolute_quantity: quantity of this ingredient in an absolute sense, e.g. 2 cups
        """
        BaseObject.__init__(self, name=name,
                            uids=uids, tags=tags, notes=notes, file_links=file_links)
        HasQuantities.__init__(self, mass_fraction=mass_fraction, volume_fraction=volume_fraction,
                               number_fraction=number_fraction, absolute_quantity=absolute_quantity
                               )

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
        from gemd.entity.object.material_spec import MaterialSpec
        from gemd.entity.link_by_uid import LinkByUID
        if material is None:
            self._material = None
        elif isinstance(material, (MaterialSpec, LinkByUID)):
            self._material = material
        else:
            raise TypeError("IngredientSpec.material must be a MaterialSpec or LinkByUID")

    @property
    def process(self):
        """Get the material."""
        return self._process

    @process.setter
    def process(self, process):
        from gemd.entity.object import ProcessSpec
        from gemd.entity.link_by_uid import LinkByUID
        if self._process is not None and isinstance(self._process, ProcessSpec):
            self._process._unset_ingredient(self)
        if process is None:
            self._process = None
        elif isinstance(process, ProcessSpec):
            self._process = process
            if not isinstance(process.ingredients, ValidList):
                process._ingredients = validate_list(self, [IngredientSpec, LinkByUID])
            else:
                process._ingredients.append(self)
        elif isinstance(process, LinkByUID):
            self._process = process
        else:
            raise TypeError("IngredientSpec.process must be a ProcessSpec or LinkByUID")

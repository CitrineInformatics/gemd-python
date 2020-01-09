import warnings

from taurus.entity.object.base_object import BaseObject
from taurus.entity.object.has_quantities import HasQuantities
from taurus.entity.setters import validate_list
from taurus.entity.valid_list import ValidList


class IngredientRun(BaseObject, HasQuantities):
    """
    An ingredient run.

    Ingredients annotate a material with information about its usage in a process.

    Parameters
    ----------
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the ingredient run.
    material: MaterialRun
        Material that this ingredient is.
    process: ProcessRun
        Process that this ingredient is used in.
    mass_fraction: :py:class:`ContinuousValue \
    <taurus.entity.value.continuous_value.ContinuousValue>`, optional
        The mass fraction of the ingredient in the process.
    volume_fraction: :py:class:`ContinuousValue \
    <taurus.entity.value.continuous_value.ContinuousValue>`, optional
        The volume fraction of the ingredient in the process.
    number_fraction: :py:class:`ContinuousValue \
    <taurus.entity.value.continuous_value.ContinuousValue>`, optional
        The number fraction of the ingredient in the process.
    absolute_quantity: :py:class:`ContinuousValue \
    <taurus.entity.value.continuous_value.ContinuousValue>`, optional
        The absolute quantity of the ingredient in the process.
    name: str, optional
        Label on the ingredient that is unique within the process that contains it.
    labels: List[str], optional
        Additional labels on the ingredient that must be unique.
    spec: IngredientSpec
        The specification of which this ingredient is a realization.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "ingredient_run"

    def __init__(self, material=None, process=None, name=None, labels=None,
                 mass_fraction=None, volume_fraction=None, number_fraction=None,
                 absolute_quantity=None,
                 spec=None, uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=name, uids=uids, tags=tags,
                            notes=notes, file_links=file_links)
        HasQuantities.__init__(self, mass_fraction, volume_fraction, number_fraction,
                               absolute_quantity)
        if name is not None:
            warnings.warn("The 'name' argument for ingredient runs is deprecated. "
                          "It may be overwritten by the name of this object's spec.",
                          DeprecationWarning)
        if labels is not None:
            warnings.warn("The 'labels' argument for ingredient runs is deprecated. "
                          "It may be overwritten by the labels of this object's spec.",
                          DeprecationWarning)
        self._material = None
        self._process = None
        self._spec = None
        self._labels = None

        self.material = material
        self.process = process
        self.labels = labels
        # this may overwrite name/labels
        self.spec = spec

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
            raise TypeError("IngredientRun.material must be a MaterialRun or "
                            "LinkByUID: {}".format(material))

    @property
    def process(self):
        """Get the material."""
        return self._process

    @process.setter
    def process(self, process):
        from taurus.entity.object import ProcessRun
        from taurus.entity.link_by_uid import LinkByUID
        if self._process is not None and isinstance(self._process, ProcessRun):
            self._process._unset_ingredient(self)
        if process is None:
            self._process = None
        elif isinstance(process, ProcessRun):
            self._process = process
            if not isinstance(process.ingredients, ValidList):
                process._ingredients = validate_list(self, [IngredientRun, LinkByUID])
            else:
                process._ingredients.append(self)
        elif isinstance(process, LinkByUID):
            self._process = process
        else:
            raise TypeError("IngredientRun.process must be a ProcessRun or "
                            "LinkByUID: {}".format(process))

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
            if isinstance(spec, IngredientSpec):
                self.name = spec.name
                self.labels = spec.labels
        else:
            raise TypeError("spec must be a IngredientSpec or LinkByUID: {}".format(spec))

    @classmethod
    def from_dict(cls, d):
        """Suppresses name/label warnings during deserializaton."""
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            return super().from_dict(d)

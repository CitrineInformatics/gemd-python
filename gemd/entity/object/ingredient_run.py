from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_quantities import HasQuantities
from gemd.entity.setters import validate_list
from gemd.entity.valid_list import ValidList


class IngredientRun(BaseObject, HasQuantities):
    """
    An ingredient run.

    Ingredients annotate a material with information about its usage in a process.

    Parameters
    ----------
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the ingredient run.
    material: MaterialRun
        Material that this ingredient is.
    process: ProcessRun
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
    spec: IngredientSpec
        The specification of which this ingredient is a realization.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "ingredient_run"

    def __init__(self, *, material=None, process=None, mass_fraction=None,
                 volume_fraction=None, number_fraction=None, absolute_quantity=None,
                 spec=None, uids=None, tags=None, notes=None, file_links=None):
        BaseObject.__init__(self, name=None, uids=uids, tags=tags,
                            notes=notes, file_links=file_links)
        HasQuantities.__init__(self, mass_fraction=mass_fraction, volume_fraction=volume_fraction,
                               number_fraction=number_fraction, absolute_quantity=absolute_quantity
                               )
        self._material = None
        self._process = None
        self._spec = None
        self._labels = None

        self.material = material
        self.process = process
        # this will overwrite name/labels if/when they are set
        self.spec = spec

    @property
    def name(self):
        """Get name."""
        from gemd.entity.object.ingredient_spec import IngredientSpec
        if isinstance(self.spec, IngredientSpec):
            return self.spec.name
        else:
            return super().name

    @name.setter
    def name(self, name):
        # This messiness is a consequence of name being an inherited attribute
        if name is not None:
            raise AttributeError("Name is set implicitly by associating with an "
                                 "IngredientSpec")
        self._name = name

    @property
    def labels(self):
        """Get labels."""
        from gemd.entity.object.ingredient_spec import IngredientSpec
        if isinstance(self.spec, IngredientSpec):
            return self.spec.labels
        else:
            return self._labels

    @property
    def material(self):
        """Get the material."""
        return self._material

    @material.setter
    def material(self, material):
        from gemd.entity.object import MaterialRun
        from gemd.entity.link_by_uid import LinkByUID
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
        from gemd.entity.object import ProcessRun
        from gemd.entity.link_by_uid import LinkByUID
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
        from gemd.entity.object.ingredient_spec import IngredientSpec
        from gemd.entity.link_by_uid import LinkByUID

        if isinstance(self._spec, IngredientSpec):  # Store values if you had them
            self._name = self.spec.name
            self._labels = validate_list(self.spec.labels, str)

        if spec is None:
            self._spec = None
        elif isinstance(spec, (IngredientSpec, LinkByUID)):
            self._spec = spec
        else:
            raise TypeError("spec must be a IngredientSpec or LinkByUID: {}".format(spec))

    @classmethod
    def from_dict(cls, d):
        """
        Overloaded method from DictSerializable to intercept `name` and `labels` fields.

        Parameters
        ----------
        d: dict
            The object as a dictionary of key-value pairs that correspond to the object's fields.

        Returns
        -------
        DictSerializable
            The deserialized object.

        """
        name = d.pop("name", None)
        labels = d.pop("labels", None)
        obj = super().from_dict(d)
        if name is not None:
            obj._name = name
        if labels is not None:
            obj._labels = validate_list(labels, str)
        return obj

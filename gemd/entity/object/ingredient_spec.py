from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_quantities import HasQuantities
from gemd.entity.setters import validate_list


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
    material: :class:`MaterialSpec <gemd.entity.object.material_spec.MaterialSpec>`
        Material that this ingredient is.
    process: :class:`ProcessSpec <gemd.entity.object.process_spec.ProcessSpec>`
        Process that this ingredient is used in.
    mass_fraction: :py:class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The mass fraction of the ingredient in the process.
    volume_fraction: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The volume fraction of the ingredient in the process.
    number_fraction: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The number fraction of the ingredient in the process.
    absolute_quantity: :class:`ContinuousValue \
    <gemd.entity.value.continuous_value.ContinuousValue>`, optional
        The absolute quantity of the ingredient in the process.
    labels: List[str], optional
        Additional labels on the ingredient that must be unique.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "ingredient_spec"

    def __init__(self, name, *, material=None, process=None, labels=None,
                 mass_fraction=None, volume_fraction=None, number_fraction=None,
                 absolute_quantity=None,
                 uids=None, tags=None, notes=None, file_links=None):

        BaseObject.__init__(self, name=name,
                            uids=uids, tags=tags, notes=notes, file_links=file_links)
        HasQuantities.__init__(self, mass_fraction=mass_fraction, volume_fraction=volume_fraction,
                               number_fraction=number_fraction, absolute_quantity=absolute_quantity
                               )

        self._material = None
        self._process = None
        self._labels = None

        self.labels = labels
        self.material = material
        self.process = process

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
        if isinstance(self._process, ProcessSpec):
            # This could throw an exception if it's not in the list, but then something else broke
            self._process.ingredients.remove(self)

        if process is None or isinstance(process, (LinkByUID, ProcessSpec)):
            self._process = process
            if isinstance(process, ProcessSpec):
                process.ingredients.append(self)
        else:
            raise TypeError("IngredientSpec.process must be a ProcessSpec or "
                            "LinkByUID: {}".format(process))

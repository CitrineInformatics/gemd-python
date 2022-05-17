from gemd.entity.object.ingredient_spec import IngredientSpec
from gemd.entity.object.material_run import MaterialRun
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.object.base_object import BaseObject
from gemd.entity.object.has_material import HasMaterial
from gemd.entity.object.has_process import HasProcess
from gemd.entity.object.has_quantities import HasQuantities
from gemd.entity.object.has_spec import HasSpec
from gemd.entity.value.continuous_value import ContinuousValue
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.file_link import FileLink
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list

from typing import Optional, Union, Iterable, List, Mapping, Type, Any


class IngredientRun(BaseObject, HasQuantities, HasSpec, HasMaterial, HasProcess):
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
    material: :class:`MaterialRun <gemd.entity.object.material_run.MaterialRun>`
        Material that this ingredient is.
    process: :class:`ProcessRun <gemd.entity.object.process_run.ProcessRun>`
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
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    """

    typ = "ingredient_run"

    def __init__(self,
                 *,
                 material: Union[MaterialRun, LinkByUID] = None,
                 process: Union[ProcessRun, LinkByUID] = None,
                 mass_fraction: ContinuousValue = None,
                 volume_fraction: ContinuousValue = None,
                 number_fraction: ContinuousValue = None,
                 absolute_quantity: ContinuousValue = None,
                 spec: Union[IngredientSpec, LinkByUID] = None,
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
        BaseObject.__init__(self, name=None, uids=uids, tags=tags,
                            notes=notes, file_links=file_links)
        self._labels = None
        HasSpec.__init__(self, spec)  # this will overwrite name/labels if/when they are set

        HasQuantities.__init__(self, mass_fraction=mass_fraction, volume_fraction=volume_fraction,
                               number_fraction=number_fraction, absolute_quantity=absolute_quantity
                               )
        self._material = None
        self._process = None

        self.material = material
        self.process = process

    @property
    def name(self) -> str:
        """Get name."""
        from gemd.entity.object.ingredient_spec import IngredientSpec
        if isinstance(self.spec, IngredientSpec):
            return self.spec.name
        else:
            return super().name

    @property
    def labels(self) -> List[str]:
        """Get labels."""
        from gemd.entity.object.ingredient_spec import IngredientSpec
        if isinstance(self.spec, IngredientSpec):
            return self.spec.labels
        else:
            return self._labels

    @property
    def material(self) -> Union[MaterialRun, LinkByUID]:
        """Get the material."""
        return self._material

    @material.setter
    def material(self, material: Union[MaterialRun, LinkByUID]):
        if material is None:
            self._material = None
        elif isinstance(material, (MaterialRun, LinkByUID)):
            self._material = material
        else:
            raise TypeError("IngredientRun.material must be a MaterialRun or "
                            "LinkByUID: {}".format(material))

    @property
    def process(self) -> Union[ProcessRun, LinkByUID]:
        """Get the material."""
        return self._process

    @process.setter
    def process(self, process: Union[ProcessRun, LinkByUID]):
        if isinstance(self._process, ProcessRun):
            # This could throw an exception if it's not in the list, but then something else broke
            self._process.ingredients.remove(self)

        if process is None or isinstance(process, (LinkByUID, ProcessRun)):
            self._process = process
            if isinstance(process, ProcessRun):
                process.ingredients.append(self)
        else:
            raise TypeError("IngredientRun.process must be a ProcessRun or "
                            "LinkByUID: {}".format(process))

    @staticmethod
    def _spec_type() -> Type:
        """Required method to satisfy HasTemplates mix-in."""
        return IngredientSpec

    @property
    def spec(self) -> Union[IngredientSpec, LinkByUID]:
        """Get the spec."""
        return super().spec

    @spec.setter
    def spec(self, spec: Union[IngredientSpec, LinkByUID]):
        """Set the spec."""
        if isinstance(self.spec, IngredientSpec):  # Store values if you had them
            self._name = self.spec.name
            self._labels = validate_list(self.spec.labels, str)
        # Note that the super() mechanism does not work properly for overloaded setters
        getattr(HasSpec, "spec").fset(self, spec)

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> DictSerializable:
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
        clean = dict(d)
        name = clean.pop("name", None)
        labels = clean.pop("labels", None)
        obj = super().from_dict(clean)
        if name is not None:
            obj._name = name
        if labels is not None:
            obj._labels = validate_list(labels, str)
        return obj

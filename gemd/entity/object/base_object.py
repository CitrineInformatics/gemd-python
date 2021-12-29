import functools

from gemd.entity.base_entity import BaseEntity
from gemd.entity.file_link import FileLink
from gemd.entity.setters import validate_list, validate_str

from typing import Optional, Union, Iterable, List, Set, Mapping


class BaseObject(BaseEntity):
    """
    Base class for objects.

    This includes {Material, Process, Measurement, Ingredient} {Run, Spec}

    Parameters
    ----------
    name: str, required
        Name of the object.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the object.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    """

    def __init__(self,
                 name: str,
                 *,
                 uids: Mapping[str, str] = None,
                 tags: Iterable[str] = None,
                 notes: str = None,
                 file_links: Optional[Union[Iterable[FileLink], FileLink]] = None):
        BaseEntity.__init__(self, uids, tags)
        self.notes = notes
        self._name = None
        self._file_links = None

        if self._attribute_has_setter("name"):
            self.name = name
        self.file_links = file_links

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _attribute_has_setter(cls, name: str) -> bool:
        """
        Internal method to identify if an attribute has a setter method.

        Necessary because IngredientRun clobbers the name setter.
        """
        prop = getattr(cls, name, None)
        return prop is None or prop.fset is not None

    @property
    def name(self) -> str:
        """Get name."""
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = validate_str(name)

    @property
    def file_links(self) -> List[FileLink]:
        """Get file links."""
        return self._file_links

    @file_links.setter
    def file_links(self, file_links: Union[Iterable[FileLink], FileLink]):
        self._file_links = validate_list(file_links, FileLink)

    def all_dependencies(self) -> Set[BaseEntity]:
        """Return a set of all immediate dependencies (no recursion)."""
        from gemd.entity.object.has_parameters import HasParameters
        from gemd.entity.object.has_conditions import HasConditions
        from gemd.entity.object.has_properties import HasProperties
        from gemd.entity.object.has_spec import HasSpec
        from gemd.entity.object.has_template import HasTemplate

        from gemd.entity.object import IngredientRun, MaterialRun, MeasurementRun  # no ProcessRun
        from gemd.entity.object import IngredientSpec, MaterialSpec  # no ProcessSpec

        result = set()

        for typ in (HasParameters, HasConditions, HasProperties, HasSpec, HasTemplate):
            if isinstance(self, typ):
                result |= typ.all_dependencies(self)
        if isinstance(self, MaterialSpec):  # is structured inconsistently
            for attr in self.properties:
                if attr.property.template is not None:
                    result.add(attr.property.template)
                for condition in attr.conditions:
                    if condition.template is not None:
                        result.add(condition.template)

        if isinstance(self, (IngredientRun, IngredientSpec, MeasurementRun)):
            if self.material is not None:
                result.add(self.material)
        if isinstance(self, (IngredientRun, IngredientSpec, MaterialRun, MaterialSpec)):
            if self.process is not None:
                result.add(self.process)

        return result

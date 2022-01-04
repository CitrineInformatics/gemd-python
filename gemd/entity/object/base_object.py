import functools

from gemd.entity.base_entity import BaseEntity
from gemd.entity.file_link import FileLink
from gemd.entity.setters import validate_list, validate_str

from typing import Optional, Union, Iterable, List, Mapping


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

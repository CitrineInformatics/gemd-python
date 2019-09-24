from taurus.entity.base_entity import BaseEntity
from taurus.entity.file_link import FileLink
from taurus.entity.setters import validate_list, validate_str


class BaseObject(BaseEntity):
    """
    Base class for objects.

    This includes {Material, Process, Measurement, Ingredient} {Run, Spec}

    Parameters
    ----------
    name: str, optional
        Name of the material spec.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/taurus-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/taurus-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the material spec.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    def __init__(self, name=None, uids=None, tags=None, notes=None, file_links=None):
        BaseEntity.__init__(self, uids, tags)
        self.notes = notes
        self._name = None
        self._file_links = None

        self.name = name
        self.file_links = file_links

    @property
    def name(self):
        """Get name."""
        return self._name

    @name.setter
    def name(self, name):
        if name is None:
            self._name = None
        else:
            self._name = validate_str(name)

    @property
    def file_links(self):
        """Get file links."""
        return self._file_links

    @file_links.setter
    def file_links(self, file_links):
        self._file_links = validate_list(file_links, FileLink)

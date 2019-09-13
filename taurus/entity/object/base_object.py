"""Base class for all Data Concepts objects."""
from taurus.entity.base_entity import BaseEntity
from taurus.entity.file_link import FileLink
from taurus.entity.setters import validate_list, validate_str


class BaseObject(BaseEntity):
    """
    Base class for objects.

    This includes {Material, Process, Measurement, Ingredient} {Run, Spec}
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

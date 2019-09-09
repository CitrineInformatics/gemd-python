"""Base class for all Data Concepts objects."""
from taurus.entity.base_entity import BaseEntity
from taurus.entity.file_link import FileLink
from taurus.entity.setters import validate_list


class BaseObject(BaseEntity):
    """
    Base class for objects.

    This includes {Material, Process, Measurement, Ingredient} {Run, Spec}
    """

    def __init__(self, uids=None, tags=None, notes=None, file_links=None):
        BaseEntity.__init__(self, uids, tags)
        self.notes = notes
        self._file_links = None
        self.file_links = file_links

    @property
    def file_links(self):
        """Get file links."""
        return self._file_links

    @file_links.setter
    def file_links(self, file_links):
        self._file_links = validate_list(file_links, FileLink)

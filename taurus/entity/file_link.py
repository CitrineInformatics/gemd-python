"""Represents a link to an external file."""
from taurus.entity.dict_serializable import DictSerializable


class FileLink(DictSerializable):
    """
    Class for storing a name and link to an external resource.

    Once the file protocol is defined, there should be substantial validation.
    """

    typ = "file_link"

    def __init__(self, filename, url):
        DictSerializable.__init__(self)
        self.filename = filename
        self.url = url

"""Represents a link to an external file."""
from gemd.entity.dict_serializable import DictSerializable


class FileLink(DictSerializable):
    """
    FileLink stores a name and link to an external resource.

    More information can be found in the
    `data model documentation \
    <https://citrineinformatics.github.io/gemd-documentation/specification/file-links/>`_

    Once the file protocol is defined, there should be substantial validation.

    Parameters
    ----------
    filename: str
        The name of the file.
    url: str
        URL that can be used to access the file.

    """

    typ = "file_link"

    def __init__(self, filename, url):
        DictSerializable.__init__(self)
        self.filename = filename
        self.url = url

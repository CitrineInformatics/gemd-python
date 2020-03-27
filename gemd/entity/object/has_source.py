"""For entities that have parameters."""
from gemd.entity.source.performed_source import PerformedSource


class HasSource(object):
    """Mixin-trait for entities that include sources (data provenance)."""

    def __init__(self, source):
        self._source = None
        self.source = source

    @property
    def source(self):
        """Get the list of parameters."""
        return self._source

    @source.setter
    def source(self, value):
        if value is None:
            self._source = None
        elif isinstance(value, PerformedSource):
            self._source = value
        else:
            raise TypeError("Source must be a PerformedSource; was {}".format(type(value)))

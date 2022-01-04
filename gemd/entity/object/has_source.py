"""For entities that have parameters."""
from gemd.entity.source.performed_source import PerformedSource


class HasSource(object):
    """Mixin-trait for entities that include sources (data provenance).

    Parameters
    ----------
    source: :class:`PerformedSource\
    <gemd.entity.source.performed_source.PerformedSource>`, optional
        Information about the person who performed the run and when.

    """

    def __init__(self, source: PerformedSource):
        self._source = None
        self.source = source

    @property
    def source(self) -> PerformedSource:
        """Get the list of parameters."""
        return self._source

    @source.setter
    def source(self, value: PerformedSource):
        if value is None:
            self._source = None
        elif isinstance(value, PerformedSource):
            self._source = value
        else:
            raise TypeError(f"Source must be a PerformedSource; was {type(value)}")

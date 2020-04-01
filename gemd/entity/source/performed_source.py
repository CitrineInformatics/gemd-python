from gemd.entity.dict_serializable import DictSerializable


class PerformedSource(DictSerializable):
    """
    Information about an activity that was performed.

    Parameters
    ----------
    performed_by: str
        The name of the person who performed the activity
    performed_date: str
        When the activity was performed as

    """

    typ = "performed_source"

    def __init__(self, performed_by=None, performed_date=None):
        self._performed_by = None
        self._performed_date = None

        self.performed_by = performed_by
        self.performed_date = performed_date

    @property
    def performed_by(self):
        """Get the name of the person who performed the activity."""
        return self._performed_by

    @performed_by.setter
    def performed_by(self, value):
        if value is None:
            self._performed_by = None
        elif isinstance(value, str):
            self._performed_by = value
        else:
            raise TypeError("performed_by must be a string")

    @property
    def performed_date(self):
        """Get when the activity was performed."""
        return self._performed_date

    @performed_date.setter
    def performed_date(self, value):
        if value is None:
            self._performed_date = None
        elif isinstance(value, str):
            self._performed_date = value
        else:
            raise TypeError("performed_date must be a string")

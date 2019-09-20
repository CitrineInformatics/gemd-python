from taurus.entity.dict_serializable import DictSerializable


class PerformedSource(DictSerializable):
    """
    Information about an activity that was performed

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

    @property
    def performed_by(self):
        return self._performed_by

    @performed_by.setter
    def performed_by(self, value):
        if not isinstance(value, str):
            raise ValueError("performed_by must be a string")
        self._performed_by = value

    @property
    def performed_date(self):
        return self._performed_date

    @performed_by.setter
    def performed_date(self, value):
        if not isinstance(value, str):
            raise ValueError("performed_date must be a string")
        self._performed_date = value

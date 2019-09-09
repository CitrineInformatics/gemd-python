"""A case-insensitive dictionary."""


class CaseInsensitiveDict(dict):
    """Extends dict so that the keys are case-insensitive."""

    def __init__(self, seq=None, **kwargs):
        super().__init__(seq or {}, **kwargs)
        self.lowercase_dict = {}
        for key in self:
            self._register_key(key)

    def __getitem__(self, key: str):
        return super().__getitem__(self.lowercase_dict[key.lower()])

    def get(self, key: str):
        """Get the value for a given case-insensitive key."""
        return self.__getitem__(key)

    def __setitem__(self, key: str, value):
        self._register_key(key)
        super().__setitem__(key, value)

    def __contains__(self, key: str):
        return self.lowercase_dict.__contains__(key.lower())

    def _register_key(self, key: str):
        prev = self.lowercase_dict.get(key.lower())
        if prev is not None and prev != key:
            raise ValueError(
                "Key '{}' already exists in dict with different case: ''".format(key, prev))
        self.lowercase_dict[key.lower()] = key

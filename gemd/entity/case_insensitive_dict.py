from typing import Tuple

_RaiseKeyError = object() # singleton for no-default behavior


class CaseInsensitiveDict(dict):
    """
    A dictionary in which the keys are case-insensitive.

    It is initialized the same way as a typical dict, but the values can be accessed without
    regard to key case. The value associated with key "Key" can also be accessed with "key"
    or "KEY" or "kEy".

    Parameters
    ----------
    seq: iterable or mapping, optional
        The key-value pairs of the dictionary. Can either be a mapping object with (key, value)
        pairs, or an iterable of tuples of the form (key, value).
    **kwargs: keyword args, optional
        An alternative way of initializing the dictionary with key-value pairs.
        Example: CaseInsensitiveDict(one=1, two="two").

    """

    def __init__(self, seq=None, **kwargs):
        super().__init__(seq or {}, **kwargs)
        self.lowercase_dict = {}
        for key in self:
            self._register_key(key)

    def __getitem__(self, key: str):
        return super().__getitem__(self.lowercase_dict[key.lower()])

    def get(self, key: str, default=None):
        """
        Get the value for a given case-insensitive key.

        Parameters
        ----------
        key: str
            The key to look up (possibly with a different casing).

        default: Any
            The result to return if the key is not present.

        Returns
        -------
        Any
            The value associated with the case-insensitive version of `key`, or None
            if `key` is not present.

        """
        if self.__contains__(key):
            return self.__getitem__(key)
        else:
            return default

    def __setitem__(self, key: str, value):
        self._register_key(key)
        super().__setitem__(key, value)

    def __contains__(self, key: str):
        return self.lowercase_dict.__contains__(key.lower())

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.lowercase_dict[key.lower()]

    def clear(self) -> None:
        super().clear()
        self.lowercase_dict.clear()

    def pop(self, key: str, default=_RaiseKeyError):
        if default is _RaiseKeyError:
            if key not in self:
                raise KeyError(key)
            val = super().pop(self.lowercase_dict[key.lower()])
        else:
            val = super().pop(self.lowercase_dict.get(key.lower()), default)
        if key in self:
            del self.lowercase_dict[key.lower()]
        return val

    def popitem(self) -> Tuple:
        result = super().popitem()
        del self.lowercase_dict[result[0].lower()]
        return result
        
    def copy(self) -> 'CaseInsensitiveDict':
        return CaseInsensitiveDict(super().copy())

    def _register_key(self, key: str):
        """
        Register a key to the dictionary.

        Check to make sure it doesn't already exist in a different case.

        Parameters
        ----------
        key: str
            The key to register.

        """
        prev = self.lowercase_dict.get(key.lower())
        if prev is not None and prev != key:
            raise ValueError(
                "Key '{}' already exists in dict with different case: '{}'".format(key, prev))
        self.lowercase_dict[key.lower()] = key

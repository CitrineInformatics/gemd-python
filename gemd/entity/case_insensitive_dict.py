from typing import Tuple, Sequence, Any, Mapping, Optional

_RaiseKeyError = object()  # singleton for no-default behavior


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

    def __init__(self, seq: Sequence = None, **kwargs) -> None:
        super().__init__(seq or {}, **kwargs)
        self.lowercase_dict = {}
        for key in self:
            self._register_key(key)

    def __getitem__(self, key: str) -> Any:
        return super().__getitem__(self.lowercase_dict[key.lower()])

    def get(self, key: str, default: Any = None) -> Any:
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

    def __setitem__(self, key: str, value: Any) -> None:
        self._register_key(key)
        super().__setitem__(key, value)

    def __contains__(self, key: str) -> bool:
        return self.lowercase_dict.__contains__(key.lower())

    def __delitem__(self, key) -> None:
        key = self.lowercase_dict.get(key.lower(), key)
        super().__delitem__(key)
        del self.lowercase_dict[key.lower()]

    def clear(self) -> None:
        """Remove all items from the dictionary."""
        super().clear()
        self.lowercase_dict.clear()

    def pop(self, key: str, default=_RaiseKeyError) -> Any:
        """
        Remove and return the value for a given key from the dictionary.

        If key is in the dictionary, remove it and return its value, else return default.
        If default is not given and key is not in the dictionary, a KeyError is raised.

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
        """
        Remove and return a (key, value) pair from the dictionary.

        popitem() is useful to destructively iterate over a dictionary, as often used
        in set algorithms.  If the dictionary is empty, calling popitem() raises a
        KeyError.

        Changed in version 3.7: LIFO order is now guaranteed. In prior versions,
        popitem() would return an arbitrary key/value pair.

        Returns
        -------
        Tuple(str, Any)
            The key-value pair

        """
        result = super().popitem()
        del self.lowercase_dict[result[0].lower()]
        return result

    def copy(self) -> 'CaseInsensitiveDict':
        """
        Return a shallow copy of the dictionary.

        Returns
        -------
        CaseInsensitiveDict
            A duplicate of the dictionary

        """
        return CaseInsensitiveDict(super().copy())

    def update(self, mapping: Optional[Mapping[str, Any]] = None, **kwargs) -> None:
        """
        Update the dictionary with the key/value pairs from other, overwriting existing keys.

        update() accepts either another dictionary object or an iterable of
        key/value pairs (as tuples or other iterables of length two). If keyword
        arguments are specified, the dictionary is then updated with those
        key/value pairs: d.update(red=1, blue=2).

        Parameters
        ----------
        mapping: Mapping
            The set of (key, value) pairs to store

        kwargs: (str, Any)
            Alternatively, the set of keyword arguments

        """
        if mapping is None:
            mapping = dict()
            no_mapping = True
        else:
            no_mapping = False
        for key in list(mapping.keys()) + list(kwargs.keys()):
            if key.lower() in self.lowercase_dict:
                prev = self.lowercase_dict[key.lower()]
                if prev != key:
                    raise ValueError(
                        "Key '{}' already exists in dict with different case: "
                        "'{}'".format(key, prev))
        if no_mapping:
            super().update(**kwargs)
        else:
            super().update(mapping, **kwargs)
        for key in list(mapping.keys()) + list(kwargs.keys()):
            self._register_key(key)

    def _register_key(self, key: str) -> None:
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

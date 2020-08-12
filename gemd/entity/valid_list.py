"""A list that can validate its contents."""
from collections.abc import Iterable


class ValidList(list):
    """
    A list-like class that verifies that its content conforms to specified types.

    Parameters
    ----------
    _list: Iterable
        The initial values for the elements of the list.
    content_type: Type or Iterable[Type]
        The allowed type(s) for the content of the list.
    trigger: function
        A function that gets invoked whenever a new element is added.
        The function will get passed the value (or each individual value in a separate
        invocation for list operations) and, if it returns something other than None,
        it will use that returned value for the assignment.

    """

    _content_type = tuple([])

    def __init__(self, _list, content_type=None, trigger=None):
        if content_type is None:
            content_type = tuple()

        if isinstance(content_type, dict):
            raise TypeError('A dict is not an acceptable container for content filters')
        elif isinstance(content_type, Iterable):
            self._content_type = tuple(content_type)
        else:
            self._content_type = tuple([content_type])
        for elem in self._content_type:
            if not isinstance(elem, type):
                raise TypeError('Content filters must be types')
        for value in _list:
            self._validate(value)

        self._trigger = None
        cache = list(_list)
        if trigger is not None:
            if not callable(trigger):
                raise TypeError('Triggers must be callable')
            self._trigger = trigger
            for i, value in enumerate(_list):
                result = self._trigger(value)
                if result is not None:
                    cache[i] = result

        list.__init__(self, cache)

    def _validate(self, value):
        """
        Validate a value against the allowed types.

        Parameters
        ----------
        value: Any
            The value to validate.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If `value` is not one of the allowed types.

        """
        if not isinstance(value, self._content_type):
            raise TypeError(
                'Value is not of an accepted type: {} =/= {}'.format(value, self._content_type))

    def __setitem__(self, index, value):
        """
        Called to implement assignment to self[index].

        Validates that `value` is one of the allowed types.

        Parameters
        ----------
        index: int
            The index of the element of the list to change
        value: Any
            The value to set the element to

        Returns
        -------
        None
            `value` is inserted into the list at position `index`, if it is valid.

        """
        self._validate(value)
        if self._trigger is not None:
            result = self._trigger(value)
            if result is not None:
                value = result
        super().__setitem__(index, value)

    def append(self, value):
        """
        Add an item to the end of the list; equivalent to a[len(a):] = [x].

        Validates that `value` is one of the allowed types.

        Parameters
        ----------
        value: Any
            The value to append at the end of the list.

        Returns
        -------
        None
            `value` is appended at the end of the list, if it is valid.

        """
        self._validate(value)
        if self._trigger is not None:
            result = self._trigger(value)
            if result is not None:
                value = result
        super().append(value)

    def extend(self, list_):
        """
        Extend the list by appending all the items in the given list; equivalent to a[len(a):] = L.

        Validates that `value` is one of the allowed types.

        Parameters
        ----------
        list_: list
            The list of values to append at the end of the list.

        Returns
        -------
        None
            `list_` is appended at the end of the list, if all its entries are valid.

        """
        if isinstance(list_, Iterable):
            for value in list_:
                self._validate(value)
        else:
            raise TypeError("'{}' object is not iterable".format(type(list_)))

        cache = list(list_)  # So that we don't edit a passed reference
        if self._trigger is not None:
            for i, value in enumerate(cache):
                result = self._trigger(value)
                if result is not None:
                    cache[i] = result

        super().extend(cache)

    def insert(self, i, value):
        """
        Insert a value at a given position, if it is one of the allowed types.

        a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x)
        is equivalent to a.append(x).

        Parameters
        ----------
        i: int
            The index of the element before which to insert.
        value: Any
            The value to insert into the list.

        Returns
        -------
        None
            `value` is inserted into the list at position `i`, if it is valid.

        """
        self._validate(value)
        if self._trigger is not None:
            result = self._trigger(value)
            if result is not None:
                value = result
        super().insert(i, value)

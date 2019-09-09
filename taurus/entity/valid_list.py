"""A list that can validate its contents."""
from collections.abc import Iterable


class ValidList(list):
    """A list-like class that verifies that its content conforms to specified types."""

    _content_type = tuple([])

    def __init__(self, _list, content_type=None, trigger=None):
        """
        Create list with content and a collection of allowed types.

        :param _list: The initial values for the elements of the list.  Must be an Iterable.
        :param content_type: A type or Iterable of types to validate the data values against.
                             If multiple elements are provided,
                             the values must be an instance of at least one of the elements.
        :param trigger: A function reference that should be invoked on any new element.
        """
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
        if trigger is not None:
            if not callable(trigger):
                raise TypeError('Triggers must be callable')
            self._trigger = trigger
            for value in _list:
                self._trigger(self, value)
        list.__init__(self, _list)

    def _validate(self, value):
        """Validate a value against the allowed types."""
        if not isinstance(value, self._content_type):
            raise TypeError(
                'Value is not of an accepted type: {} =/= {}'.format(value, self._content_type))

    def __setitem__(self, index, value):
        """
        Called to implement assignment to self[index].

        Necessary to override to insert value validation.

        :param index: The element of the list to change
        :param value: The value to set the element to
        :return: no return
        """
        self._validate(value)
        if self._trigger is not None:
            self._trigger(self, value)
        super().__setitem__(index, value)

    def append(self, value):
        """
        Add an item to the end of the list; equivalent to a[len(a):] = [x].

        Necessary to override to insert value validation.
        """
        self._validate(value)
        if self._trigger is not None:
            self._trigger(self, value)
        super().append(value)

    def extend(self, list_):
        """
        Extend the list by appending all the items in the given list; equivalent to a[len(a):] = L.

        Necessary to override to insert value validation.
        """
        if isinstance(list_, Iterable):
            for value in list_:
                self._validate(value)
        else:
            raise TypeError("'{}' object is not iterable".format(type(list_)))
        if self._trigger is not None:
            for value in list_:
                self._trigger(self, value)
        super().extend(list_)

    def insert(self, i, value):
        """
        Insert an item at a given position.

        The first argument is the index of the element before which to insert,
        so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x)
        is equivalent to a.append(x).

        Necessary to override to insert value validation.
        """
        self._validate(value)
        if self._trigger is not None:
            self._trigger(self, value)
        super().insert(i, value)

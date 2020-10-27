"""Base class for all values."""
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.bounds.base_bounds import BaseBounds

from abc import abstractmethod


class BaseValue(DictSerializable):
    """
    Base class for all values.

    "Value" is a generic term for the information contained in an
    :class:`attribute <gemd.entity.attribute.base_attribute.BaseAttribute>`.
    A value may be one of the following types: `RealValue`, `IntegerValue`, `Categorical`.
    """

    typ = "value"

    @abstractmethod
    def _to_bounds(self) -> BaseBounds:
        """
        Return the smallest bounds object that is consistent with the Value.

        Returns
        -------
        BaseBounds
            The minimally consistent
            :class:`bounds <gemd.entity.bounds.base_bounds.BaseBounds>`.

        """

"""Base class for all bounds."""
from abc import abstractmethod

from taurus.entity.dict_serializable import DictSerializable


class BaseBounds(DictSerializable):
    """Base class for bounds, including RealBounds and CategoricalBounds."""

    @abstractmethod
    def contains(self, bounds):
        """
        Check if another bounds is contained within this bounds.

        Parameters
        ----------
        bounds: BaseBounds
            Other bounds object to check.

        Returns
        -------
        bool
            True if any value that validates true for bounds also validates true for this

        """
        if bounds is None:
            return False
        if isinstance(bounds, BaseBounds):
            return True
        raise TypeError('{} is not a Bounds object'.format(bounds))

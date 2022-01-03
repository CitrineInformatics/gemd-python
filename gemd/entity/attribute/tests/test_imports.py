# Need * to make sure we're hitting collisions if they could happen
from gemd import *  # noqa: F401, F403


class ImportTestObj:
    """A class that has a property."""

    @property
    def test_property(self):
        """A property to validate decorator functionality."""
        Property(name='Trial')  # noqa: F405
        return True


def test_imports():
    """* used to import property, which shadowed @property."""
    assert ImportTestObj().test_property

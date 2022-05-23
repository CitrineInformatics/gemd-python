from gemd.util import cached_isinstance

from typing import List, Iterable


def test_cached_isinstance():
    """Verify that cached_isinstance is operating as exepcted."""
    passing_pairs = [
        ("one", str),
        (1, int),
        ("one", (str, int)),
        ([1, 2, 3], List),
        ("one", Iterable),
    ]
    for obj, cls in passing_pairs:
        assert isinstance(obj, cls) == cached_isinstance(obj, cls)
        # Twice, for good measure, because we're caching
        assert isinstance(obj, cls) == cached_isinstance(obj, cls)

    failing_pairs = [
        ("one", int),
        (1, str),
        ("one", (float, int)),
        ("one", List),
        (1, Iterable),
    ]
    for obj, cls in failing_pairs:
        assert isinstance(obj, cls) == cached_isinstance(obj, cls)
        # Twice, for good measure, because we're caching
        assert isinstance(obj, cls) == cached_isinstance(obj, cls)

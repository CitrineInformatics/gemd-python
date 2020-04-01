"""All possible types of samples."""
from gemd.enumeration.base_enumeration import BaseEnumeration


class SampleType(BaseEnumeration):
    """Enumeration containing all possible sample types for a MaterialRun."""

    EXPERIMENTAL = "experimental"
    PRODUCTION = "production"
    VIRTUAL = "virtual"
    UNKNOWN = "unknown"

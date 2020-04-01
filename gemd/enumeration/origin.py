"""All possible origins of an attribute."""
from gemd.enumeration.base_enumeration import BaseEnumeration


class Origin(BaseEnumeration):
    """Enumeration containing all possible origins for an attribute."""

    MEASURED = "measured"
    PREDICTED = "predicted"
    SUMMARY = "summary"
    SPECIFIED = "specified"
    COMPUTED = "computed"
    UNKNOWN = "unknown"

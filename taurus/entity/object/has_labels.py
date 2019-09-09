"""For entities that have unique_labels and labels."""
from taurus.entity.setters import validate_list, validate_str


class HasLabels(object):
    """Mix-in trait for entities that include unique_label and labels."""

    def __init__(self, unique_label=None, labels=None):
        self._labels = None
        self.labels = labels

        self._unique_label = None
        self.unique_label = unique_label

    @property
    def unique_label(self):
        """Get unique labels."""
        return self._unique_label

    @unique_label.setter
    def unique_label(self, unique_label):
        if unique_label is None:
            self._unique_label = None
        else:
            self._unique_label = validate_str(unique_label)

    @property
    def labels(self):
        """Get labels."""
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = validate_list(labels, str)

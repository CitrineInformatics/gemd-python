"""A process template."""
from taurus.entity.object import ProcessRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.setters import validate_list
from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.template.has_condition_templates import HasConditionTemplates
from taurus.entity.template.has_parameter_templates import HasParameterTemplates


class ProcessTemplate(BaseTemplate, HasConditionTemplates, HasParameterTemplates):
    """Template for processes, containing parameter, and condition templates and ranges."""

    typ = "process_template"

    def __init__(self, name=None, description=None,
                 conditions=None, parameters=None,
                 allowed_names=None, allowed_labels=None,
                 uids=None, tags=None):
        BaseTemplate.__init__(self, name, description, uids, tags)
        HasConditionTemplates.__init__(self, conditions)
        HasParameterTemplates.__init__(self, parameters)

        self._allowed_names = None
        self.allowed_names = allowed_names

        self._allowed_labels = None
        self.allowed_labels = allowed_labels

    @property
    def allowed_names(self):
        """Get the allowed names."""
        return self._allowed_names

    @allowed_names.setter
    def allowed_names(self, allowed_names):
        # if none, leave as none; don't set to the empty set
        if allowed_names is None:
            self._allowed_names = allowed_names
        else:
            self._allowed_names = validate_list(allowed_names, str)

    @property
    def allowed_labels(self):
        """Get the allowed labels."""
        return self._allowed_labels

    @allowed_labels.setter
    def allowed_labels(self, allowed_labels):
        # if none, leave as none; don't set to the empty set
        if allowed_labels is None:
            self._allowed_labels = allowed_labels
        else:
            self._allowed_labels = validate_list(allowed_labels, str)

    def validate(self, process):
        """Check that a process satisfies all condition and parameter templates."""
        if not isinstance(process, (ProcessRun, ProcessSpec)):
            raise ValueError("ProcessTemplate can only be applied to Processes")

        self.validate_conditions(process)
        self.validate_parameters(process)

        # Check the name namespace
        if self.allowed_names is not None:
            unique_names = {x.name
                            for x in process.ingredients if x.name is not None}
            extra = unique_names.difference(set(self.allowed_names))
            if len(extra) > 0:
                raise ValueError("Found disallowed names: {}".format(extra))

        # Check the label namespace
        if self.allowed_labels is not None:
            labels = {label for x in process.ingredients for label in x.labels}
            extra = labels.difference(set(self.allowed_labels))
            if len(extra) > 0:
                raise ValueError("Found disallowed labels: {}".format(extra))

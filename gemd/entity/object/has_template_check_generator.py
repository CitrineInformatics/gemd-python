"""For entities that have specs."""
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.bounds_validation import get_validation_level, WarningLevel
from gemd.entity.dict_serializable import logger

from abc import ABC, abstractmethod
from inspect import getmodule, getmembers, isclass, signature
from typing import Union, Callable, TypeVar

T = TypeVar('T')


class HasTemplateCheckGenerator(ABC):
    """Mix-in trait for objects that can generate a Check Template closure."""

    @property
    @abstractmethod
    def template(self) -> Union[BaseTemplate, LinkByUID]:
        """Get the object template associated with this object."""

    def _generate_template_check(self,
                                 validate: Callable[["HasTemplateCheckGenerator", T], bool]
                                 ) -> Callable[[T], None]:
        """
        Generate a closure for the object and the validation routine.

        Parameters
        ----------
        validate: function(HasTemplateCheckGenerator, Attribute) -> bool
            A method that checks if the object template is consistent with the attribute

        Returns
        -------
        function(Attribute)
            If the attribute is inconsistent, ignores, warns or dies based on get_validation_level

        Raises
        ------
        ValueError
            If `value` is not one of the allowed types or if mapping types fails.

        """
        # Determine which class `validate` is from, so we can type check the object template
        module = getmodule(validate)  # Get the module that contains `validate`
        # Get the class that was defined in this module (a.k.a. not imported)
        cls = next((y for x, y in getmembers(module, isclass) if getmodule(y) == module), None)
        if cls is None:
            raise ValueError(f"Could not map class for function {validate}.")

        # Grab the type of validate's argument so we know what kind of attribute we are validating
        arguments = list(signature(validate).parameters.values())  # List of arguments to validate
        attr = arguments[1].annotation if len(arguments) == 2 else None  # First self, then attr
        if attr is None:
            raise ValueError(f"Could not map attribute for function {validate}.")

        def template_check(x: attr):
            """Given an attribute, check it against this object's template."""
            level = get_validation_level()
            reject = level != WarningLevel.IGNORE \
                and isinstance(self.template, cls) \
                and not validate(self.template, x)

            if reject:
                message = f"Value {x.value} is inconsistent with template {self.template.name}"
                if level == WarningLevel.WARNING:
                    logger.warning(message)
                else:
                    raise ValueError(message)

        return template_check

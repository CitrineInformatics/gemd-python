from gemd.entity.base_entity import BaseEntity
from gemd.entity.file_link import FileLink
from gemd.entity.setters import validate_list, validate_str


class BaseObject(BaseEntity):
    """
    Base class for objects.

    This includes {Material, Process, Measurement, Ingredient} {Run, Spec}

    Parameters
    ----------
    name: str, required
        Name of the object.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-documentation/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-documentation/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the object.
    file_links: List[:class:`FileLink <gemd.entity.file_link.FileLink>`], optional
        Links to associated files, with resource paths into the files API.

    """

    def __init__(self, name, *, uids=None, tags=None, notes=None, file_links=None):
        BaseEntity.__init__(self, uids, tags)
        self.notes = notes
        self._name = None
        self._file_links = None

        self.name = name
        self.file_links = file_links

    @property
    def name(self):
        """Get name."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = validate_str(name)

    @property
    def file_links(self):
        """Get file links."""
        return self._file_links

    @file_links.setter
    def file_links(self, file_links):
        self._file_links = validate_list(file_links, FileLink)

    def all_dependences(self):
        """Return a set of all immediate dependencies (no recursion)."""
        from gemd.entity.object.has_parameters import HasParameters
        from gemd.entity.object.has_conditions import HasConditions
        from gemd.entity.object.has_properties import HasProperties
        from gemd.entity.object.has_template import HasTemplate

        from gemd.entity.object import IngredientRun, MaterialRun, MeasurementRun, ProcessRun
        from gemd.entity.object import IngredientSpec, MaterialSpec  # no ProcessSpec

        result = set()

        if isinstance(self, HasParameters):
            for attr in self.parameters:
                if attr.template is not None:
                    result.add(attr.template)
        if isinstance(self, HasConditions):
            for attr in self.conditions:
                if attr.template is not None:
                    result.add(attr.template)
        if isinstance(self, HasProperties):
            for attr in self.properties:
                if attr.template is not None:
                    result.add(attr.template)
        if isinstance(self, MaterialSpec):  # is structured inconsistently
            for attr in self.properties:
                if attr.property.template is not None:
                    result.add(attr.property.template)
                for condition in attr.conditions:
                    if condition.template is not None:
                        result.add(condition.template)

        if isinstance(self, HasTemplate):
            if self.template is not None:
                result.add(self.template)
        if isinstance(self, (IngredientRun, MaterialRun, MeasurementRun, ProcessRun)):
            if self.spec is not None:
                result.add(self.spec)
        if isinstance(self, (IngredientRun, IngredientSpec, MeasurementRun)):
            if self.material is not None:
                result.add(self.material)
        if isinstance(self, (IngredientRun, IngredientSpec, MaterialRun, MaterialSpec)):
            if self.process is not None:
                result.add(self.process)

        return result

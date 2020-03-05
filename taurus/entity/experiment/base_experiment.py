from taurus.entity.base_entity import BaseEntity

from taurus.entity.template.base_template import BaseTemplate
from taurus.entity.object.base_object import BaseObject


class BaseExperiment(BaseEntity):
    """An experiment is a collection of Taurus objects, with defined connections between them.
    """

    def __init__(self, objects, connections, uids, tags):
        BaseEntity.__init__(self, uids=uids, tags=tags)
        self._objects = None
        self._connections = None

        self.objects = objects
        self.connections = connections

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        for obj in objects.values():
            assert isinstance(obj, (BaseTemplate, BaseObject))
        self._objects = objects

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def connections(self, connections):
        self._connections = connections  # TODO: check all str in objects mapping

    def visualize(self):
        """Graphs the objects in this data model."""
        from dagre_py.core import plot
        nodes = [{"label": p} for p in self.templates.keys()]
        edges = [{"source": s, "target": t} for s, t in self.connections]
        plot({"nodes": nodes, "edges": edges})

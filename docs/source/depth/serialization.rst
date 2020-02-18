.. _Serialization In Depth:

==============================
Serialization (with Graphs!)
==============================

Taurus objects link together to form graphs with directional edges.
For example, a :class:`~taurus.entity.object.material_run.MaterialRun` links back to the :class:`~taurus.entity.object.process_run.ProcessRun` that produced it.
Some of these links are bi-directional.
For example, a :class:`~taurus.entity.object.process_run.ProcessRun` also links forward to the :class:`~taurus.entity.object.material_run.MaterialRun` that it produces, if there is one.
Other links are uni-directional.
For example, a :class:`~taurus.entity.object.material_run.MaterialRun` links to its :class:`~taurus.entity.object.material_spec.MaterialSpec` but that :class:`~taurus.entity.object.material_spec.MaterialSpec` doesn't link back.
Uni-directional links are typically used when the multiplicity of a relationship can be large.
For example, a material may be referenced in thousands of ingredients.

In taurus, bi-directional links are readable but only a single direction is writable.
For example, a :class:`~taurus.entity.object.measurement_run.MeasurementRun` can set the :class:`~taurus.entity.object.material_run.MaterialRun` material that it was performed on,
but a :class:`~taurus.entity.object.material_run.MaterialRun` cannot set the :class:`~taurus.entity.object.measurement_run.MeasurementRun`s it contains.
Each time a :class:`~taurus.entity.object.measurement_run.MeasurementRun`'s ``material`` field is set,
that :class:`~taurus.entity.object.material_run.MaterialRun` has the :class:`~taurus.entity.object.measurement_run.MeasurementRun` appended to its ``measurements`` field.

This linking structure presents several challenges for serialization and deserialization:

a. The graph cannot be traversed through uni-directional links in the wrong direction.
b. Only the writeable side of bi-directional links can be persisted.
c. Objects that are referenced by multiple objects must be deserialized to the same object.

These challenges are addressed by a custom json serialization procedure and the special :class:`~taurus.entity.link_by_uid.LinkByUID` class.

1. Each entity that doesn't already have at least one unique identifier is assigned a unique identifier so it can be referenced.
2. The graph is flattened by traversing it while maintaining a seen list and replacing object references to other entities with :class:`~taurus.entity.link_by_uid.LinkByUID` objects, producing the set of entities that are reachable.
3. The objects are sorted into a special "writable" order that ensures that link targets are created when deserializing.
4. This sorted list of entities is assigned to the "context" field in the serialization output.
5. The original object (which may contain multiple entities) is assigned to the "object" field in the serialization output.
6. The serialization output is serialized with a special :class:`~json.JSONEncoder`, :class:`~taurus.json.taurus_encoder.TaurusEncoder`, that skips the soft side of links.

Here's an example of the serialized output for a :class:`~taurus.entity.object.material_spec.MaterialSpec` and :class:`~taurus.entity.object.process_spec.ProcessSpec`:

::

  {
    "context": [
      {
        "conditions": [],
        "file_links": [],
        "name": "producing process",
        "notes": null,
        "parameters": [],
        "tags": [],
        "template": null,
        "type": "process_spec",
        "uids": {
          "auto": "a103b759-b3e9-472e-8ec1-c69ee5d1981a"
        }
      },
      {
        "file_links": [],
        "name": "Produced material",
        "notes": null,
        "process": {
          "id": "a103b759-b3e9-472e-8ec1-c69ee5d1981a",
          "scope": "auto",
          "type": "link_by_uid"
        },
        "properties": [],
        "tags": [],
        "template": null,
        "type": "material_spec",
        "uids": {
          "auto": "ad2c31ab-e8c0-40f1-a1b6-c5b5950026cd"
        }
      }
    ],
    "object": {
      "id": "ad2c31ab-e8c0-40f1-a1b6-c5b5950026cd",
      "scope": "auto",
      "type": "link_by_uid"
    }
  }

The deserialization is a comparatively simple two-step process.
First, the string or file is deserialized with python's builtin deserializer and a custom object hook.
This hook does three things:
it knows how to build taurus entities and other :class:`~taurus.entity.dict_serializable.DictSerializable` objects,
it creates an index with the unique identifiers of the taurus entities that it has seen so far,
and it replaces any :class:`~taurus.entity.link_by_uid.LinkByUID` that it encounters with objects from that index.
The only thing left to do is return the ``"object"`` item from the resulting dictionary.

This strategy is implemented in the :class:`~taurus.json.taurus_json.TaurusJson` class
and conveniently exposed in the :py:mod:`taurus.json` module, which provides the familiar `json` interface.
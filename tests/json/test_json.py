"""Test serialization and deserialization of gemd objects."""
import json as json_builtin
from copy import deepcopy
from uuid import uuid4

import pytest

from gemd.json import GEMDJson
import gemd.json as gemd_json
from gemd.entity.attribute.property import Property
from gemd.entity.bounds.real_bounds import RealBounds
from gemd.entity.case_insensitive_dict import CaseInsensitiveDict
from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.dict_serializable import DictSerializable
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.object import MeasurementRun, MaterialRun, ProcessRun
from gemd.entity.object import MeasurementSpec, MaterialSpec, ProcessSpec
from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.object.ingredient_spec import IngredientSpec
from gemd.entity.template.property_template import PropertyTemplate
from gemd.entity.value.nominal_integer import NominalInteger
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.value.normal_real import NormalReal
from gemd.enumeration.origin import Origin
from gemd.util import substitute_objects, substitute_links


def test_serialize():
    """Serializing a nested object should be identical to individually serializing each piece."""
    condition = Condition(name="A condition", value=NominalReal(7, ''))
    parameter = Parameter(name="A parameter", value=NormalReal(mean=17, std=1, units=''))
    input_material = MaterialRun("name", tags="input")
    process = ProcessRun("name", tags="A tag on a process run")
    ingredient = IngredientRun(material=input_material, process=process)
    material = MaterialRun("name", tags=["A tag on a material"], process=process)
    measurement = MeasurementRun("name", tags="A tag on a measurement", conditions=condition,
                                 parameters=parameter, material=material)

    # serialize the root of the tree
    native_object = json_builtin.loads(gemd_json.dumps(measurement))
    # ingredients don't get serialized on the process
    assert(len(native_object["context"]) == 5)
    assert(native_object["object"]["type"] == LinkByUID.typ)

    # serialize all the nodes
    native_batch = json_builtin.loads(gemd_json.dumps([material, process, measurement, ingredient]))
    assert(len(native_batch["context"]) == 5)
    assert(len(native_batch["object"]) == 4)
    assert(all(x["type"] == LinkByUID.typ for x in native_batch["object"]))


def test_deserialize():
    """Round-trip serde should leave the object unchanged."""
    condition = Condition(name="A condition", value=NominalReal(7, ''))
    parameter = Parameter(name="A parameter", value=NormalReal(mean=17, std=1, units=''))
    measurement = MeasurementRun("name",
                                 tags="A tag on a measurement",
                                 conditions=condition,
                                 parameters=parameter)
    copy_meas = GEMDJson().copy(measurement)
    assert(copy_meas.conditions[0].value == measurement.conditions[0].value)
    assert(copy_meas.parameters[0].value == measurement.parameters[0].value)
    assert(copy_meas.uids["auto"] == measurement.uids["auto"])


def test_uuid_serde():
    """Any UUIDs in uids & LinkByUIDs shouldn't break stuff."""
    process = ProcessSpec(name="A process", uids={"uuid": uuid4(), "word": "turnbuckle"})
    copy_proc = GEMDJson().copy(process)
    assert all(copy_proc.uids[scope] == str(process.uids.get(scope)) for scope in copy_proc.uids)
    assert len(copy_proc.uids) == len(process.uids)

    link = LinkByUID(id=uuid4(), scope="mine")
    assert GEMDJson().copy(link).id == str(link.id)


def test_scope_control():
    """Serializing a nested object should be identical to individually serializing each piece."""
    input_material = MaterialSpec("input_material")
    process = ProcessSpec("process")
    IngredientSpec("ingredient", material=input_material, process=process)
    material = MaterialSpec("name", process=process)

    # Verify the default scope is there
    default_json = GEMDJson()
    default_text = default_json.dumps(material)
    assert "auto" in default_text
    assert "custom" not in default_text

    # Clear out ids
    input_material.uids = {}
    process.uids = {}
    process.ingredients[0].uids = {}
    input_material.uids = {}
    material.uids = {}

    # Verify the default scope is there
    custom_json = GEMDJson(scope='custom')
    custom_text = custom_json.dumps(material)
    assert "auto" not in custom_text
    assert "custom" in custom_text


def test_deserialize_extra_fields():
    """Extra JSON fields should be ignored in deserialization."""
    json_data = '{"context": [],' \
                ' "object": {"nominal": 5, "type": "nominal_integer", "extra garbage": "foo"}}'
    assert(gemd_json.loads(json_data) == NominalInteger(nominal=5))


def test_enumeration_serde():
    """An enumeration should get serialized as a string."""
    condition = Condition(name="A condition", notes=Origin.UNKNOWN)
    copy_condition = GEMDJson().copy(condition)
    assert copy_condition.notes == Origin.UNKNOWN.value
    assert not isinstance(copy_condition.notes, Origin)


def test_attribute_serde():
    """An attribute with a link to an attribute template should be copy-able."""
    prop_tmpl = PropertyTemplate(name='prop_tmpl',
                                 bounds=RealBounds(0, 2, 'm')
                                 )
    prop = Property(name='prop',
                    template=prop_tmpl,
                    value=NominalReal(1, 'm')
                    )
    meas_spec = MeasurementSpec("a spec")
    meas = MeasurementRun("a measurement", spec=meas_spec, properties=[prop])
    assert gemd_json.loads(gemd_json.dumps(prop)) == prop
    assert gemd_json.loads(gemd_json.dumps(meas)) == meas
    assert isinstance(prop.template, PropertyTemplate)


def test_thin_dumps():
    """Test that thin_dumps turns pointers into links."""
    mat = MaterialRun("The actual material")
    meas_spec = MeasurementSpec("measurement", uids={'my_scope': '324324'})
    meas = MeasurementRun("The measurement", spec=meas_spec, material=mat)

    thin_copy = MeasurementRun.build(json_builtin.loads(GEMDJson().thin_dumps(meas)))
    assert isinstance(thin_copy, MeasurementRun)
    assert isinstance(thin_copy.material, LinkByUID)
    assert isinstance(thin_copy.spec, LinkByUID)
    assert thin_copy.spec.id == meas_spec.uids['my_scope']

    # Check that LinkByUID objects are correctly converted their JSON equivalent
    expected_json = '{"id": "my_id", "scope": "scope", "type": "link_by_uid"}'
    assert GEMDJson().thin_dumps(LinkByUID('scope', 'my_id')) == expected_json

    # Check that objects lacking .uid attributes will raise an exception when dumped
    with pytest.raises(TypeError):
        GEMDJson().thin_dumps({{'key': 'value'}})


def test_uid_deser():
    """Test that uids continue to be a CaseInsensitiveDict after deserialization."""
    material = MaterialRun("Input material", tags="input", uids={'Sample ID': '500-B'})
    ingredient = IngredientRun(material=material)
    ingredient_copy = gemd_json.loads(gemd_json.dumps(ingredient))
    assert isinstance(ingredient_copy.uids, CaseInsensitiveDict)
    assert ingredient_copy.material == material
    assert ingredient_copy.material.uids['sample id'] == material.uids['Sample ID']


def test_unexpected_serialization():
    """Trying to serialize an unexpected class should throw a TypeError."""
    class DummyClass:
        def __init__(self, foo):
            self.foo = foo

    with pytest.raises(TypeError):
        gemd_json.dumps(ProcessRun("A process", notes=DummyClass("something")))


def test_unexpected_deserialization():
    """Trying to deserialize an unexpected class should throw a TypeError."""
    # DummyClass cannot be serialized since dumps will round-robin serialize
    # in the substitute_links method
    with pytest.raises(TypeError):
        gemd_json.dumps(ProcessRun("A process", notes={"type": "unknown"}))


def test_register_classes_override():
    """Test that register_classes overrides existing entries in the class index."""
    class MyProcessSpec(ProcessSpec):
        pass

    normal = GEMDJson()
    custom = GEMDJson()

    obj = ProcessSpec(name="foo")
    assert not isinstance(normal.copy(obj), MyProcessSpec),\
        "Class registration bled across GEMDJson() objects"

    assert isinstance(custom.copy(obj), ProcessSpec),\
        "Custom GEMDJson didn't deserialize as MyProcessSpec"


def test_pure_substitutions():
    """Make sure substitute methods don't mutate inputs."""
    json_str = '''
          [
            [
              {
                "uids": {
                  "id": "9118c2d3-1c38-47fe-a650-c2b92fdb6777"
                },
                "type": "material_run",
                "name": "flour"
              }
            ],
            {
              "type": "ingredient_run",
              "uids": {
                "id": "8858805f-ec02-49e4-ba3b-d784e2aea3f8"
              },
              "material": {
                "type": "link_by_uid",
                "scope": "ID",
                "id": "9118c2d3-1c38-47fe-a650-c2b92fdb6777"
              },
              "process": {
                "type": "link_by_uid",
                "scope": "ID",
                "id": "9148c2d3-2c38-47fe-b650-c2b92fdb6777"
              }
            }
          ]
       '''
    index = {}
    clazz_index = DictSerializable.class_mapping
    original = json_builtin.loads(json_str, object_hook=lambda x: GEMDJson()._load_and_index(x, index, clazz_index))
    frozen = deepcopy(original)
    loaded = substitute_objects(original, index)
    assert original == frozen
    frozen_loaded = deepcopy(loaded)
    substitute_links(loaded)
    assert loaded == frozen_loaded
    for o in loaded:
        substitute_links(o)
    assert loaded == frozen_loaded


def test_case_insensitive_rehydration():
    """

    Test that loads() can connect id scopes with different cases.

    This situation should not occur in gemd on its own, but faraday returns LinkOrElse objects
    with the default scope "ID", whereas citrine-python assigns ids with the scope "id".
    The uids dictionary is supposed to be case-insensitive, so rehydration should still work.
    """
    # A simple json string that could be loaded, representing an ingredient linked to a material.
    # The material link has "scope": "ID", whereas the material in the context list, which is
    # to be loaded, has uid with scope "id".
    json_str = '''
          {
            "context": [
              {
                "uids": {
                  "id": "9118c2d3-1c38-47fe-a650-c2b92fdb6777"
                },
                "type": "material_run",
                "name": "flour"
              }
            ],
            "object": {
              "type": "ingredient_run",
              "uids": {
                "id": "8858805f-ec02-49e4-ba3b-d784e2aea3f8"
              },
              "material": {
                "type": "link_by_uid",
                "scope": "ID",
                "id": "9118c2d3-1c38-47fe-a650-c2b92fdb6777"
              },
              "process": {
                "type": "link_by_uid",
                "scope": "ID",
                "id": "9148c2d3-2c38-47fe-b650-c2b92fdb6777"
              }
            }
          }
       '''
    loaded_ingredient = gemd_json.loads(json_str)
    # The ingredient's material will either be a MaterialRun (pass) or a LinkByUID (fail)
    assert isinstance(loaded_ingredient.material, MaterialRun)


def test_many_ingredients():
    """Test that ingredients remain connected to processes when round-robined through json."""
    proc = ProcessRun("foo", spec=ProcessSpec("sfoo"))
    expected = []
    for i in range(10):
        mat = MaterialRun(name=str(i), spec=MaterialSpec("s{}".format(i)))
        i_spec = IngredientSpec(name="i{}".format(i), material=mat.spec, process=proc.spec)
        IngredientRun(process=proc, material=mat, spec=i_spec)
        expected.append("i{}".format(i))

    reloaded = gemd_json.loads(gemd_json.dumps(proc))
    assert len(list(reloaded.ingredients)) == 10
    names = [x.name for x in reloaded.ingredients]
    assert sorted(names) == sorted(expected)


def test_deeply_nested_rehydration():
    """
    Tests that loads fully replaces links with objects.

    In particular, this test makes sure that loads is robust to objects being referenced by
    LinkByUid before they are "declared" in the JSON array.
    """
    json_str = '''
{
  "context": [
    {
      "type": "process_spec",
      "parameters": [
        {
          "type": "parameter",
          "name": "oven",
          "value": {
            "type": "nominal_categorical",
            "category": "oven 1"
          },
          "template": {
            "type": "link_by_uid",
            "scope": "id",
            "id": "536a3ebb-55a4-4560-a6df-fba44cdb917a"
          },
          "origin": "unknown",
          "file_links": []
        }
      ],
      "conditions": [],
      "uids": {
        "id": "f77dc327-ef44-4a39-a617-061ace5fa789"
      },
      "tags": [],
      "name": "Ideal baking",
      "file_links": []
    },
    {
      "type": "process_run",
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "f77dc327-ef44-4a39-a617-061ace5fa789"
      },
      "parameters": [
        {
          "type": "parameter",
          "name": "oven",
          "value": {
            "type": "nominal_categorical",
            "category": "oven 1"
          },
          "template": {
            "type": "link_by_uid",
            "scope": "id",
            "id": "536a3ebb-55a4-4560-a6df-fba44cdb917a"
          },
          "origin": "unknown",
          "file_links": []
        }
      ],
      "conditions": [],
      "uids": {
        "id": "7cb9471b-0c90-4fd9-bfe1-0e9d7602ab0d",
        "my_id": "jvkzrlnm"
      },
      "tags": [
        "cake::yes"
      ],
      "name": "cake baking",
      "file_links": []
    },
    {
      "type": "material_spec",
      "properties": [],
      "uids": {
        "id": "230fc837-8a19-402c-86ad-e451b7a80f9d"
      },
      "tags": [],
      "name": "Flour",
      "file_links": []
    },
    {
      "type": "material_spec",
      "process": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "f77dc327-ef44-4a39-a617-061ace5fa789"
      },
      "properties": [],
      "uids": {
        "id": "b935aa7d-93a4-407f-937f-cca32d7a8413"
      },
      "tags": [],
      "name": "An ideal cake",
      "file_links": []
    },
    {
      "type": "material_spec",
      "properties": [
        {
          "property": {
            "type": "property",
            "name": "mass",
            "value": {
              "type": "normal_real",
              "mean": 0.84,
              "std": 0.04,
              "units": "gram"
            },
            "template": {
              "type": "link_by_uid",
              "scope": "id",
              "id": "3b46b191-b3d0-4b31-bdba-377cca315cbd"
            },
            "origin": "unknown",
            "file_links": []
          },
          "conditions": [
            {
              "type": "condition",
              "name": "temperature",
              "value": {
                "type": "nominal_real",
                "nominal": 20,
                "units": "degC"
              },
              "template": {
                "type": "link_by_uid",
                "scope": "id",
                "id": "09fb94ab-17fb-4428-a20e-d6b0d0ae5fb2"
              },
              "origin": "unknown",
              "file_links": []
            }
          ],
          "type": "property_and_conditions"
        }
      ],
      "uids": {
        "id": "39ec0605-0b9b-443c-ab6a-4d7bc1b73b24"
      },
      "tags": [],
      "name": "Butter",
      "file_links": []
    },
    {
      "type": "ingredient_spec",
      "name": "Shortening",
      "material": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "39ec0605-0b9b-443c-ab6a-4d7bc1b73b24"
      },
      "process": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "f77dc327-ef44-4a39-a617-061ace5fa789"
      },
      "labels": [],
      "uids": {
        "id": "118eacb7-6edc-4e57-b40b-2971481d37e5"
      },
      "tags": [],
      "file_links": []
    },
    {
      "type": "ingredient_spec",
      "name": "Flour",
      "material": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "230fc837-8a19-402c-86ad-e451b7a80f9d"
      },
      "process": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "f77dc327-ef44-4a39-a617-061ace5fa789"
      },
      "labels": [],
      "absolute_quantity": {
        "type": "normal_real",
        "mean": 500,
        "std": 50,
        "units": "gram"
      },
      "uids": {
        "id": "f694d2cc-5b00-42ef-92b7-dee3cdc7239a"
      },
      "tags": [],
      "file_links": []
    },
    {
      "type": "material_run",
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "230fc837-8a19-402c-86ad-e451b7a80f9d"
      },
      "sample_type": "unknown",
      "uids": {
        "id": "76185e4f-c778-4654-a2ae-cc49851e291f"
      },
      "tags": [],
      "name": "Flour",
      "file_links": []
    },
        {
      "type": "material_run",
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "39ec0605-0b9b-443c-ab6a-4d7bc1b73b24"
      },
      "sample_type": "unknown",
      "uids": {
        "id": "605bf096-3b2d-4c3b-afaf-f77bcff9806f"
      },
      "tags": [],
      "name": "Butter",
      "file_links": []
    },{
      "type": "material_run",
      "process": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "7cb9471b-0c90-4fd9-bfe1-0e9d7602ab0d"
      },
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "b935aa7d-93a4-407f-937f-cca32d7a8413"
      },
      "sample_type": "unknown",
      "uids": {
        "id": "f0f41fb9-32dc-4903-aaf4-f369de71530f"
      },
      "tags": [],
      "name": "A cake",
      "file_links": []
    },
    {
      "type": "ingredient_run",
      "material": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "76185e4f-c778-4654-a2ae-cc49851e291f"
      },
      "process": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "7cb9471b-0c90-4fd9-bfe1-0e9d7602ab0d"
      },
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "f694d2cc-5b00-42ef-92b7-dee3cdc7239a"
      },
      "name": "500 g flour",
      "labels": [],
      "uids": {
        "id": "36aa5bff-c89d-43fa-95c8-fa6b710061d8"
      },
      "tags": [],
      "file_links": []
    },
    {
      "type": "ingredient_run",
      "material": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "605bf096-3b2d-4c3b-afaf-f77bcff9806f"
      },
      "process": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "7cb9471b-0c90-4fd9-bfe1-0e9d7602ab0d"
      },
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "118eacb7-6edc-4e57-b40b-2971481d37e5"
      },
      "name": "1 stick butter",
      "labels": [],
      "absolute_quantity": {
        "type": "nominal_real",
        "nominal": 1,
        "units": "dimensionless"
      },
      "uids": {
        "id": "91ab45f2-ceec-4109-8f74-2f9964a4bc2c"
      },
      "tags": [],
      "file_links": []
    },
    {
      "type": "measurement_spec",
      "parameters": [],
      "conditions": [],
      "uids": {
        "id": "85c911eb-af5a-4c34-9b59-b88b84780239"
      },
      "tags": [],
      "name": "Tasty spec",
      "file_links": []
    },
    {
      "type": "measurement_run",
      "spec": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "85c911eb-af5a-4c34-9b59-b88b84780239"
      },
      "material": {
        "type": "link_by_uid",
        "scope": "id",
        "id": "f0f41fb9-32dc-4903-aaf4-f369de71530f"
      },
      "properties": [],
      "parameters": [],
      "conditions": [],
      "uids": {
        "id": "9673f15d-76df-4dcd-a409-7152cb629a3f"
      },
      "tags": [
        "example::tag"
      ],
      "name": "Tastiness",
      "notes": "it is tasty",
      "file_links": []
    }
  ],
  "object": {
    "type": "link_by_uid",
    "scope": "id",
    "id": "f0f41fb9-32dc-4903-aaf4-f369de71530f"
  }
}
    '''
    material_history = gemd_json.loads(json_str)
    assert isinstance(material_history.process.ingredients[1].spec, IngredientSpec)
    assert isinstance(material_history.measurements[0], MeasurementRun)

    copied = gemd_json.loads(gemd_json.dumps(material_history))
    assert isinstance(copied.process.ingredients[1].spec, IngredientSpec)
    assert isinstance(copied.measurements[0], MeasurementRun)

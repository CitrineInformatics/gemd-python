"""Test serialization and deserialization of taurus objects."""
from taurus.client.json_encoder import dumps, loads
from taurus.entity.case_insensitive_dict import CaseInsensitiveDict
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object import MeasurementRun, MaterialRun, ProcessRun
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal

import json


def test_serialize():
    """Serializing a nested object should be identical to individually serializing each piece."""
    condition = Condition(name="A condition", value=NominalReal(7, ''))
    parameter = Parameter(name="A parameter", value=NormalReal(mean=17, std=1, units=''))
    input_material = MaterialRun(tags="input")
    process = ProcessRun(tags="A tag on a process run")
    _ = IngredientRun(material=input_material, process=process)
    material = MaterialRun(tags=["A tag on a material"], process=process)
    measurement = MeasurementRun(tags="A tag on a measurement", conditions=condition,
                                 parameters=parameter, material=material)

    # serialize the root of the tree
    native_object = json.loads(dumps(measurement))
    assert(len(native_object[0]) == 5)
    assert(native_object[1]["type"] == LinkByUID.typ)

    # serialize all of the nodes
    native_batch = json.loads(dumps([material, process, measurement, input_material]))
    assert(len(native_batch[0]) == 5)
    assert(len(native_batch[1]) == 4)
    assert(all(x["type"] == LinkByUID.typ for x in native_batch[1]))

    # check that we get the same preface by serializing the root of the tree as all the nodes
    assert(native_object[0] == native_batch[0])


def test_deserialize():
    """Round-trip serde should leave the object unchanged."""
    condition = Condition(name="A condition", value=NominalReal(7, ''))
    parameter = Parameter(name="A parameter", value=NormalReal(mean=17, std=1, units=''))
    measurement = MeasurementRun(tags="A tag on a measurement", conditions=condition,
                                 parameters=parameter)
    copy = loads(dumps(measurement))
    assert(copy.conditions[0].value == measurement.conditions[0].value)
    assert(copy.parameters[0].value == measurement.parameters[0].value)
    assert(copy.uids["auto"] == measurement.uids["auto"])


def test_uid_deser():
    """Test that uids continue to be a CaseInsensitiveDict after deserialization."""
    material = MaterialRun("Input material", tags="input", uids={'Sample ID': '500-B'})
    ingredient = IngredientRun(material=material)
    ingredient_copy = loads(dumps(ingredient))
    assert isinstance(ingredient_copy.uids, CaseInsensitiveDict)
    assert ingredient_copy.material == material
    assert ingredient_copy.material.uids['sample id'] == material.uids['Sample ID']


def test_case_insensitive_rehydration():
    """

    Test that loads() can connect id scopes with different cases.

    This situation should not occur in taurus on its own, but faraday returns LinkOrElse objects
    with the default scope "ID", whereas citrine-python assigns ids with the scope "id".
    The uids dictionary is supposed to be case-insensitive, so rehydration should still work.
    """
    # A simple json string that could be loaded, representing an ingredient linked to a material.
    # The material link has "scope": "ID", whereas the material in the context list, which is
    # to be loaded, has uid with scope "id".
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
    loaded_ingredient = loads(json_str)
    # The ingredient's material will either be a MaterialRun (pass) or a LinkByUID (fail)
    assert isinstance(loaded_ingredient.material, MaterialRun)


def test_deeply_nested_rehydration():
    """
    Tests that loads fully replaces links with objects.

    In particular, this test makes sure that loads is robust to objects being referenced by
    LinkByUid before they are "declared" in the JSON array.
    """
    json_str = '''
[
  [
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
      "unique_label": "500 g flour",
      "labels": [],
      "uids": {
        "id": "36aa5bff-c89d-43fa-95c8-fa6b710061d8"
      },
      "tags": [],
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
      "unique_label": "1 stick butter",
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
      "type": "ingredient_spec",
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
  {
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
  }
]
    '''
    material_history = loads(json_str)
    assert isinstance(material_history.process.ingredients[1].spec, IngredientSpec)
    assert isinstance(material_history.measurements[0], MeasurementRun)

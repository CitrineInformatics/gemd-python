"""Test serialization and deserialization of taurus objects."""
from taurus.client.json_encoder import dumps, loads
from taurus.entity.case_insensitive_dict import CaseInsensitiveDict
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object import MeasurementRun, MaterialRun, ProcessRun
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal

import json


def test_serialize():
    """Serializing a nested object should be identical to individually serializing each piece."""
    condition = Condition(name="A condition", value=NominalReal(7, ''))
    parameter = Parameter(name="A parameter", value=NormalReal(mean=17, std=1, units=''))
    input_material = MaterialRun(tags="input")
    input_ingredient = IngredientRun(material=input_material)
    process = ProcessRun(tags="A tag on a process run", ingredients=[input_ingredient])
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
              }
            }
          ]
       '''
    loaded_ingredient = loads(json_str)
    # The ingredient's material will either be a MaterialRun (pass) or a LinkByUID (fail)
    assert isinstance(loaded_ingredient.material, MaterialRun)

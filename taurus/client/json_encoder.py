"""Encoding and decoding taurus objects to/from json."""
import json
from json import JSONEncoder

from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.attribute.property import Property
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions
from taurus.entity.base_entity import BaseEntity
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.composition_bounds import CompositionBounds
from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.dict_serializable import DictSerializable
from taurus.entity.file_link import FileLink
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object import ProcessRun, MaterialRun, MeasurementRun
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate
from taurus.entity.template.parameter_template import ParameterTemplate
from taurus.entity.template.process_template import ProcessTemplate
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.empirical_formula import EmpiricalFormula
from taurus.entity.value.nominal_categorical import NominalCategorical
from taurus.entity.value.nominal_composition import NominalComposition
from taurus.entity.value.nominal_integer import NominalInteger
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.entity.value.uniform_integer import UniformInteger
from taurus.entity.value.uniform_real import UniformReal
from taurus.enumeration.base_enumeration import BaseEnumeration
from taurus.util import flatten, substitute_links, deepcopy, set_uuids


def dumps(obj, **kwargs):
    """Dump an taurus object, or container of them, into a json-formatting string."""
    # create a top level list of [flattened_objects, link-i-fied return value]
    res = [obj]
    additional = flatten(res)
    substitute_links(res)
    res.insert(0, additional)
    return json.dumps(res, cls=TaurusEncoder, sort_keys=True, **kwargs)


def loads(json_str, **kwargs):
    """Deserialize a json-formatted string into taurus objects."""
    # Create an index to hold the objects by their uid reference
    # so we can replace links with pointers
    index = {}
    raw = json.loads(json_str, object_hook=lambda x: _loado(x, index), **kwargs)
    # the return value is in the 2nd position.
    return raw[1]


def load(fp, **kwargs):
    """Read the file as string and call loads."""
    return loads(fp.read(), **kwargs)


def dump(obj, fp, **kwargs):
    """Call dumps and then write the result to fp."""
    fp.write(dumps(obj, **kwargs))
    return


def thin_dumps(obj, **kwargs):
    """Thin the object by substituting in links, and then dumps only that object."""
    if not isinstance(obj, BaseEntity):
        raise ValueError("Can only dump BaseEntities, but got {}".format(type(obj)))

    set_uuids(obj)
    res = deepcopy(obj)
    substitute_links(res)
    return json.dumps(res, cls=TaurusEncoder, sort_keys=True, **kwargs)


def copy(obj):
    """Copy an object by dumping and then loading it."""
    return loads(dumps(obj))


# build index from the class's typ member to the class itself
_clazzes = [
    MaterialTemplate, MeasurementTemplate, ProcessTemplate,
    MaterialSpec, MeasurementSpec, ProcessSpec, IngredientSpec,
    ProcessRun, MaterialRun, MeasurementRun, IngredientRun,
    Property, Condition, Parameter, PropertyAndConditions,
    PropertyTemplate, ConditionTemplate, ParameterTemplate,
    RealBounds, IntegerBounds, CategoricalBounds, CompositionBounds,
    NominalComposition, EmpiricalFormula,
    NominalReal, UniformReal, NormalReal, DiscreteCategorical, NominalCategorical,
    UniformInteger, NominalInteger,
    FileLink
]
_clazz_index = {}
for clazz in _clazzes:
    _clazz_index[clazz.typ] = clazz


def _loado(d, index):
    if "type" not in d:
        return d
    typ = d.pop("type")

    if typ in _clazz_index:
        clz = _clazz_index[typ]
        obj = clz.from_dict(d)
    elif typ == LinkByUID.typ:
        obj = LinkByUID.from_dict(d)
        if (obj.scope.lower(), obj.id) in index:
            return index[(obj.scope.lower(), obj.id)]
        return obj
    else:
        raise ValueError("Unexpected base object type: {}".format(typ))

    if isinstance(obj, BaseEntity):
        for (scope, id) in obj.uids.items():
            index[(scope.lower(), id)] = obj
    return obj


class TaurusEncoder(JSONEncoder):
    """Rules for encoding taurus objects as json strings."""

    def default(self, o):
        """Default encoder implementation."""
        if isinstance(o, DictSerializable):
            return o.as_dict()
        elif isinstance(o, BaseEnumeration):
            return o.value
        else:
            return JSONEncoder.default(self, o)

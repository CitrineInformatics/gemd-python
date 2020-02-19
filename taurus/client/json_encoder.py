# flake8: noqa
"""Encoding and decoding taurus objects to/from json."""
import deprecation
import taurus
from taurus.json import TaurusEncoder, TaurusJson


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.dumps instead")
def dumps(obj, **kwargs):
    return taurus.json.dumps(obj, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.loads instead")
def loads(json_str, **kwargs):
    return taurus.json.loads(json_str, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.load instead")
def load(fp, **kwargs):
    return taurus.json.load(fp, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.dump instead")
def dump(obj, fp, **kwargs):
    return taurus.json.dump(obj, fp, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.TaurusJson().raw_dumps instead")
def raw_dumps(obj, **kwargs):
    return TaurusJson().raw_dumps(obj, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.TaurusJson().thin_dumps instead")
def thin_dumps(obj, **kwargs):
    return TaurusJson().thin_dumps(obj, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.TaurusJson().raw_loads instead")
def raw_loads(json_str, **kwargs):
    return TaurusJson().raw_loads(json_str, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use taurus.json.TaurusJson().copy instead")
def copy(obj):
    return TaurusJson().copy(obj)

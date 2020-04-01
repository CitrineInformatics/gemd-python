# flake8: noqa
"""Encoding and decoding gemd objects to/from json."""
import deprecation
import gemd
from gemd.json import GEMDEncoder, GEMDJson


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.dumps instead")
def dumps(obj, **kwargs):
    return gemd.json.dumps(obj, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.loads instead")
def loads(json_str, **kwargs):
    return gemd.json.loads(json_str, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.load instead")
def load(fp, **kwargs):
    return gemd.json.load(fp, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.dump instead")
def dump(obj, fp, **kwargs):
    return gemd.json.dump(obj, fp, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.GEMDJson().raw_dumps instead")
def raw_dumps(obj, **kwargs):
    return GEMDJson().raw_dumps(obj, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.GEMDJson().thin_dumps instead")
def thin_dumps(obj, **kwargs):
    return GEMDJson().thin_dumps(obj, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.GEMDJson().raw_loads instead")
def raw_loads(json_str, **kwargs):
    return GEMDJson().raw_loads(json_str, **kwargs)


@deprecation.deprecated(deprecated_in="0.6.0", removed_in="0.7.0",
                        details="Use gemd.json.GEMDJson().copy instead")
def copy(obj):
    return GEMDJson().copy(obj)

"""Utility methods."""
from gemd.util import recursive_foreach

from typing import List, Dict, Any


def make_instance(base_spec):
    """
    Create a set of Run objects that mimic the connectivity of the passed Spec object.

    Parameters
    ---------
    base_spec: BaseObject
        A spec instance that may point to other specs.

    Returns
    -------
    BaseObject
        The run instance that is created, and may point to other runs.

    """
    seen = dict()

    def crawler(spec):
        from gemd.entity.object.measurement_spec import MeasurementSpec
        from gemd.entity.object.measurement_run import MeasurementRun
        from gemd.entity.object.material_spec import MaterialSpec
        from gemd.entity.object.material_run import MaterialRun
        from gemd.entity.object.ingredient_spec import IngredientSpec
        from gemd.entity.object.ingredient_run import IngredientRun
        from gemd.entity.object.process_spec import ProcessSpec
        from gemd.entity.object.process_run import ProcessRun

        if id(spec) in seen:
            return seen[id(spec)]

        if isinstance(spec, MeasurementSpec):
            seen[id(spec)] = MeasurementRun(
                name=spec.name,
                spec=spec
            )
        elif isinstance(spec, MaterialSpec):
            seen[id(spec)] = MaterialRun(
                name=spec.name,
                spec=spec
            )
            seen[id(spec)].process = crawler(spec.process) if spec.process else None
        elif isinstance(spec, IngredientSpec):
            seen[id(spec)] = IngredientRun(spec=spec)
            seen[id(spec)].material = crawler(spec.material) if spec.material else None
        elif isinstance(spec, ProcessSpec):
            seen[id(spec)] = ProcessRun(
                name=spec.name,
                spec=spec
            )
            for x in spec.ingredients:
                crawler(x).process = seen[id(spec)]
        else:
            raise TypeError('Passed object is not a spec-like object({})'.format(type(spec)))

        # Should we assume that the same MaterialSpec in different parts of the tree
        # yields the same MaterialRun?
        return seen[id(spec)]

    return crawler(base_spec)


# Global to support array_like
_array_like = None


def array_like():
    """
    Figure out what kinds of list-like things we should be supporting for list type-checks.

    Returns
    -------
    tuple
        A tuple of supported array-like classes.

    """
    global _array_like
    if _array_like is not None:
        return _array_like
    try:
        import numpy as np
        try:
            import pandas as pd
            _array_like = (list, tuple, np.ndarray, pd.core.base.PandasObject)
        except ImportError:  # pragma: no cover
            _array_like = (list, tuple, np.ndarray)  # pragma: no cover
    except ImportError:  # pragma: no cover
        _array_like = (list, tuple)  # pragma: no cover

    return _array_like


def complete_material_history(mat) -> List[Dict[str, Any]]:
    """
    Get a list of every single object in the material history, all as dictionaries.

    This is useful for testing, if we want the context list that can be used to rehydrate
    an entire material history.

    Parameters
    ---------
    mat: MaterialRun
        root material run
    Returns
    -------
    list
        a list containing every object connected to mat, each a dictionary with
        all links substituted.

    """
    from gemd.entity.base_entity import BaseEntity
    import json
    from gemd.json import dumps, loads
    from gemd.util.impl import substitute_links

    result = []

    def body(obj: BaseEntity):
        copy = substitute_links(loads(dumps(obj)))
        result.append(json.loads(dumps(copy))["context"][0])

    recursive_foreach(mat, body, apply_first=False)

    return result

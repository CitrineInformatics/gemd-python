"""Utility methods."""


def make_instance(base_spec):
    """
    Create a set of Run objects that mimic the connectivity of the passed Spec object.

    Paramters
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
        from taurus.entity.object.measurement_spec import MeasurementSpec
        from taurus.entity.object.measurement_run import MeasurementRun
        from taurus.entity.object.material_spec import MaterialSpec
        from taurus.entity.object.material_run import MaterialRun
        from taurus.entity.object.ingredient_spec import IngredientSpec
        from taurus.entity.object.ingredient_run import IngredientRun
        from taurus.entity.object.process_spec import ProcessSpec
        from taurus.entity.object.process_run import ProcessRun

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
            seen[id(spec)] = IngredientRun(name=spec.name, spec=spec)
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


def complete_material_history(mat):
    """
    Get a list of every single object in the material history, all as dictionaries.

    This is useful for testing, if we want the context list that can be used to rehydrate
    an entire material history.

    :param mat: root material run
    :return: a list containing every object connected to mat, each a dictionary with all
        links substituted.
    """
    from taurus.entity.base_entity import BaseEntity
    from taurus.entity.dict_serializable import DictSerializable
    import json
    from taurus.client.json_encoder import dumps, loads
    from taurus.util.impl import substitute_links

    queue = [mat]
    seen = set()
    result = []

    while queue:
        obj = queue.pop(0)

        if isinstance(obj, BaseEntity):
            if obj not in seen:
                seen.add(obj)
                queue.extend(obj.__dict__.values())

                copy = loads(dumps(obj))
                substitute_links(copy)
                result.insert(0, json.loads(dumps(copy))[0][0])  # Leaf first
        elif isinstance(obj, (list, tuple)):
            queue.extend(obj)
        elif isinstance(obj, dict):
            queue.extend(obj.values())
        elif isinstance(obj, DictSerializable):
            queue.extend(obj.__dict__.values())

    return result

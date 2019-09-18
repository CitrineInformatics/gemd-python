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
        except ImportError:
            _array_like = (list, tuple, np.ndarray)
    except ImportError:
        _array_like = (list, tuple)

    return _array_like

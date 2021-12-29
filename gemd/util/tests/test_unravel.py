from gemd.entity.attribute import Condition, Parameter
from gemd.entity.bounds import IntegerBounds
from gemd.entity.object import ProcessSpec, ProcessRun, MaterialSpec, MaterialRun, \
    MeasurementRun, IngredientSpec
from gemd.entity.template import ProcessTemplate, ConditionTemplate, ParameterTemplate
from gemd.entity.value import NominalInteger
from gemd.util import unravel


def test_unravel():
    """Verify collection of contained BaseEntities."""
    cond_tmpl = ConditionTemplate("Condition", bounds=IntegerBounds(1, 10))
    param_tmpl = ParameterTemplate("Parameter", bounds=IntegerBounds(1, 10))
    proc_tmpl = ProcessTemplate("pt", parameters=[param_tmpl])
    mat_spec = MaterialSpec("ms", process=ProcessSpec("ps", template=proc_tmpl))
    mat_run = MaterialRun("mr", process=ProcessRun("pr", spec=mat_spec.process), spec=mat_spec)
    mat_spec.process.parameters.append(Parameter("Parameter",
                                                 value=NominalInteger(5),
                                                 template=param_tmpl))
    mat_run.process.conditions.append(Condition("Condition",
                                                value=NominalInteger(5),
                                                template=cond_tmpl))
    msr = MeasurementRun("msr", material=mat_run, parameters=[Parameter("Parameter",
                                                                        value=NominalInteger(5),
                                                                        template=param_tmpl)])
    ing_spec = IngredientSpec("is", material=mat_spec, process=mat_spec.process)

    lst = unravel(mat_run)
    assert cond_tmpl in lst, "ConditionTemplate not found."
    assert param_tmpl in lst, "ParameterTemplate not found."
    assert proc_tmpl in lst, "ProcessTemplate not found."
    assert mat_spec in lst, "MaterialSpec not found."
    assert mat_run in lst, "MaterialRun not found."
    assert mat_spec.process in lst, "ProcessSpec not found."
    assert mat_run.process in lst, "ProcessRun not found."
    assert msr in lst, "MeasurementRun not found."
    assert ing_spec in lst, "IngredientSpec not found."
    assert len(lst) == 9, "Expected 9 objects in list."

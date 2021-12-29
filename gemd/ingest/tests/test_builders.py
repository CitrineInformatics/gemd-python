from gemd.ingest import make_node, add_edge, add_attribute, add_measurement
from gemd.entity.template import ProcessTemplate, MaterialTemplate, MeasurementTemplate, \
    PropertyTemplate, ConditionTemplate, ParameterTemplate
from gemd.entity.bounds import RealBounds, IntegerBounds, CategoricalBounds, \
    CompositionBounds, MolecularStructureBounds
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.value import EmpiricalFormula

import pytest


class UnsupportedBounds(BaseBounds):
    """Dummy class to provide an invalid bounds type."""

    def contains(self, bounds):  # pragma: no cover
        """Only here to satisfy abstract method."""
        super().contains(bounds)


def test_build():
    """Test builder routines."""
    mix_tmpl = ProcessTemplate(name="Mixing")
    term_tmpl = MaterialTemplate(name="Terminal")
    procure_tmpl = ProcessTemplate(name="Procure")
    raw_tmpl = MaterialTemplate(name="Raw")

    prop_tmpl = PropertyTemplate(name="Property", bounds=RealBounds(0, 10, "m"))
    cond_tmpl = ConditionTemplate(name="Condition", bounds=CategoricalBounds(["a", "b", "c"]))
    param_tmpl = ParameterTemplate(name="Parameter",
                                   bounds=CompositionBounds(EmpiricalFormula.all_elements()))
    mol_tmpl = PropertyTemplate(name="Molecule", bounds=MolecularStructureBounds())
    int_tmpl = ConditionTemplate(name="Integer", bounds=IntegerBounds(0, 10))
    bad_tmpl = PropertyTemplate(name="Bad", bounds=UnsupportedBounds())

    root = make_node(name="Root", material_template=term_tmpl, process_template=mix_tmpl)
    assert root.template == term_tmpl, "Object didn't link correctly."
    assert root.process.template == mix_tmpl, "Object didn't link correctly."
    one = make_node("One", material_template=raw_tmpl, process_template=procure_tmpl)
    add_edge(output_material=root, input_material=one)
    add_edge(output_material=root,
             input_material=make_node("Two")
             )
    assert len(root.process.ingredients) == 2, "Ingredient count didn't line up."

    # Attribute tests
    with pytest.raises(ValueError):
        add_attribute(one.spec, cond_tmpl, "b")  # No property yet

    # Create a property-and-condition on the mat spec
    add_attribute(one.spec, prop_tmpl, 1)
    assert len(one.spec.properties) == 1, "Material spec didn't get a property."
    assert one.spec.properties[0].property.template == prop_tmpl, "Wrong linking on property."
    assert one.spec.properties[0].property.value.units == "meter", "Wrong units on property."
    assert one.spec.properties[0].property.value.nominal == 1, "Wrong value on property."
    add_attribute(one.spec, cond_tmpl, "b")
    assert len(one.spec.properties[0].conditions) == 1, "Wrong location on condition."
    assert one.spec.properties[0].conditions[0].template == cond_tmpl, \
        "Wrong linking on condition."
    assert one.spec.properties[0].conditions[0].value.category == "b", "Wrong value on condition."
    with pytest.raises(ValueError):
        add_attribute(one.spec, param_tmpl, "H2O")  # Mat Specs don't support parameters

    # Create a second property-and-condition on the mat spec
    add_attribute(one.spec, mol_tmpl, "C")
    assert len(one.spec.properties) == 2, "Second property added."
    add_attribute(one.spec, int_tmpl, 5)
    assert len(one.spec.properties[-1].conditions) == 1, "Second property has a condition."

    # Attach a measurement
    msr_tmpl = MeasurementTemplate(name="Measure!", properties=[prop_tmpl])
    msr = add_measurement(material=root, template=msr_tmpl)
    assert len(root.measurements) == 1, "Measurement was added to root."
    add_attribute(msr, cond_tmpl, "c")  # Order shouldn't matter anymore
    assert len(msr.conditions) == 1, "Condition wasn't added to measurement."
    add_attribute(msr, prop_tmpl, 5)
    assert len(msr.properties) == 1, "Property wasn't added to measurement."
    add_attribute(msr, param_tmpl, "CH4")
    assert len(msr.parameters) == 1, "Parameter wasn't added to measurement."
    assert msr.parameters[0].template == param_tmpl, "Wrong linking on parameter."
    assert msr.parameters[0].value.formula == "CH4", "Wrong value on parameter."

    # Test failed builds
    with pytest.raises(ValueError):
        add_measurement(material=root)
    assert len(root.measurements) == 1, "Failed measurement build still added an object."
    with pytest.raises(ValueError):
        add_attribute(msr, bad_tmpl, "Word")
    assert len(msr.properties) == 1, "Failed attribute build still added an object."
    with pytest.raises(ValueError):
        add_attribute(root.process, prop_tmpl, 9)
    assert len(root.process.conditions) == 0, "Failed attribute build still added an object."
    assert len(root.process.parameters) == 0, "Failed attribute build still added an object."

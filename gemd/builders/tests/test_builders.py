from gemd.builders import make_node, add_edge, add_measurement, add_attribute, \
    make_attribute
from gemd.entity.attribute.base_attribute import BaseAttribute
from gemd.entity.object import MaterialRun
from gemd.entity.template import ProcessTemplate, MaterialTemplate, MeasurementTemplate, \
    PropertyTemplate, ConditionTemplate, ParameterTemplate
from gemd.entity.template.attribute_template import AttributeTemplate
from gemd.entity.bounds import RealBounds, IntegerBounds, CategoricalBounds, \
    CompositionBounds, MolecularStructureBounds
from gemd.entity.bounds.base_bounds import BaseBounds
from gemd.entity.value import EmpiricalFormula, NominalReal
from gemd.entity.link_by_uid import LinkByUID
from gemd.units import parse_units

import pytest


class UnsupportedBounds(BaseBounds):
    """Dummy object to test Bounds type checking."""

    def contains(self, bounds):  # pragma: no cover
        """Only here to satisfy abstract method."""
        super().contains(bounds)


class UnsupportedAttribute(BaseAttribute):
    """Dummy object to test Attribute type checking."""


class UnsupportedAttributeTemplate(AttributeTemplate):
    """Dummy object to test Attribute type checking."""


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


def test_quantities():
    """Exercise the expressions on quantity in add_edge."""
    ing_one = add_edge(make_node("Input"),
                       make_node("Output"),
                       mass_fraction=0.1,
                       number_fraction=0.2,
                       volume_fraction=0.3,
                       absolute_quantity=0.4,
                       absolute_units='kg')

    assert ing_one.mass_fraction.nominal == 0.1, "Mass fraction got set."
    assert ing_one.number_fraction.nominal == 0.2, "Number fraction got set."
    assert ing_one.volume_fraction.nominal == 0.3, "Volume fraction got set."
    assert ing_one.absolute_quantity.nominal == 0.4, "Absolute quantity got set."
    assert ing_one.absolute_quantity.units == parse_units('kg'), "Absolute units got set."

    ing_two = add_edge(make_node("Input"),
                       make_node("Output"),
                       mass_fraction=NominalReal(0.5, ''),
                       number_fraction=NominalReal(0.6, ''),
                       volume_fraction=NominalReal(0.7, ''),
                       absolute_quantity=NominalReal(0.8, 'liters'))

    assert ing_two.mass_fraction.nominal == 0.5, "Mass fraction got set."
    assert ing_two.number_fraction.nominal == 0.6, "Number fraction got set."
    assert ing_two.volume_fraction.nominal == 0.7, "Volume fraction got set."
    assert ing_two.absolute_quantity.nominal == 0.8, "Absolute quantity got set."
    assert ing_two.absolute_quantity.units == parse_units('liters'), "Absolute units got set."

    with pytest.raises(ValueError):
        add_edge(make_node("Input"), make_node("Output"), absolute_quantity=0.4)
    with pytest.raises(ValueError):
        add_edge(make_node("Input"), make_node("Output"),
                 absolute_quantity=NominalReal(0.8, 'liters'), absolute_units='liters')


def test_attributes():
    """Exercise permutations of attributes, bounds and values."""
    prop_tmpl = PropertyTemplate(name="Property", bounds=RealBounds(0, 10, "m"))
    cond_tmpl = ConditionTemplate(name="Condition", bounds=CategoricalBounds(["a", "b", "c"]))
    param_tmpl = ParameterTemplate(name="Parameter",
                                   bounds=CompositionBounds(EmpiricalFormula.all_elements()))
    mol_tmpl = PropertyTemplate(name="Molecule", bounds=MolecularStructureBounds())
    int_tmpl = ConditionTemplate(name="Integer", bounds=IntegerBounds(0, 10))

    msr = add_measurement(make_node('Material'),
                          name='Measurement',
                          attributes=[make_attribute(prop_tmpl, 5),
                                      make_attribute(cond_tmpl, 'a'),
                                      make_attribute(param_tmpl, 'SiC'),
                                      make_attribute(mol_tmpl, 'InChI=1S/CSi/c1-2'),
                                      make_attribute(mol_tmpl, '[C-]#[Si+]'),
                                      make_attribute(int_tmpl, 5)
                                      ])
    assert msr.properties[0].value.nominal == 5
    assert msr.conditions[0].value.category == 'a'
    assert msr.parameters[0].value.formula == 'SiC'
    assert msr.properties[1].value.inchi == 'InChI=1S/CSi/c1-2'
    assert msr.properties[2].value.smiles == '[C-]#[Si+]'
    assert msr.conditions[1].value.nominal == 5


def test_exceptions():
    """Additional tests to get full coverage on exceptions."""
    with pytest.raises(ValueError):
        add_edge(MaterialRun("Input"), make_node("Output"))

    with pytest.raises(ValueError):
        add_edge(make_node("Input"), MaterialRun("Output", spec=LinkByUID("Bad", "ID")))

    with pytest.raises(ValueError):
        add_measurement(make_node('Material'),
                        name='Measurement',
                        attributes=[UnsupportedAttribute("Spider-man")])

    with pytest.raises(ValueError):
        make_attribute(UnsupportedAttributeTemplate, 5)

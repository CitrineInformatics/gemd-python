"""Bake a cake."""
import json

from taurus.client.json_encoder import thin_dumps
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.attribute.property import Property
from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.object.ingredient_spec import IngredientSpec
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.material_spec import MaterialSpec
from taurus.entity.object.measurement_run import MeasurementRun
from taurus.entity.object.measurement_spec import MeasurementSpec
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.object.process_spec import ProcessSpec
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.material_template import MaterialTemplate
from taurus.entity.template.measurement_template import MeasurementTemplate
from taurus.entity.template.parameter_template import ParameterTemplate
from taurus.entity.template.process_template import ProcessTemplate
from taurus.entity.template.property_template import PropertyTemplate
from taurus.entity.value.nominal_integer import NominalInteger
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.enumeration.origin import Origin
from taurus.util.impl import set_uuids
from taurus.entity.util import complete_material_history


def make_cake_templates():
    """Define all templates independently, since in the wild this will be an independent operation"""
    tmpl = dict()

    # Attributes
    tmpl['Cooking time'] = ConditionTemplate(
        name="Cooking time",
        bounds=RealBounds(0, 7 * 24.0, "hr")
    )
    tmpl["Oven temperature setting"] = ParameterTemplate(
        name="Oven temperature setting",
        bounds=RealBounds(0, 2000.0, "K")
    )
    tmpl["Oven temperature"] = ConditionTemplate(
        name="Oven temperature",
        bounds=RealBounds(0, 2000.0, "K")
    )

    tmpl["Tastiness"] = PropertyTemplate(
        name="Tastiness",
        bounds=IntegerBounds(lower_bound=1, upper_bound=10)
    )

    # Objects
    tmpl["Baking in an oven"] = ProcessTemplate(
        name="Baking in an oven",
        conditions=[(tmpl["Oven temperature"], RealBounds(0, 700, "degF"))],
        parameters=[(tmpl["Oven temperature setting"], RealBounds(100, 550, "degF"))]
    )

    tmpl["Taste test"] = MeasurementTemplate(
        properties=[tmpl["Tastiness"]]
    )

    tmpl["Dessert"] = MaterialTemplate(
        name="Dessert",
        properties=[tmpl["Tastiness"]]
    )

    return tmpl


def make_cake():
    """Define all objects that go into making a demo cake."""
    ######################################################################
    # Templates
    tmpl = make_cake_templates()

    ######################################################################
    # Objects
    cake = MaterialRun(name='Cake')

    baked = MaterialRun(name='Baked Cake')
    frosting = MaterialRun(name='Frosting')

    batter = MaterialRun(name='Batter')

    wetmix = MaterialRun(name='Wet Mix')
    drymix = MaterialRun(name='Dry Mix')

    flour = MaterialRun(name='Flour')
    baking_powder = MaterialRun(name='Baking Powder')
    salt = MaterialRun(name='Salt')
    sugar = MaterialRun(name='Sugar')
    butter = MaterialRun(name='Butter')
    eggs = MaterialRun(name='Eggs')
    vanilla = MaterialRun(name='Vanilla')
    milk = MaterialRun(name='Milk')
    chocolate = MaterialRun(name='Chocolate')
    powder_sugar = MaterialRun(name='Powdered Sugar')

    cake.process = ProcessRun(name='Icing')
    for ingredient in (baked, frosting):
        IngredientRun(name='{} input'.format(ingredient.name),
                      material=ingredient, process=cake.process)

    cake_taste = MeasurementRun(name='Final Taste', material=cake)
    cake_appearance = MeasurementRun(name='Final Appearance', material=cake)

    baked.process = ProcessRun(name='Baking')
    IngredientRun(name='{} input'.format(ingredient.name),
                  material=batter, process=baked.process)

    batter.process = ProcessRun(name='Mixing Batter')
    for ingredient in (wetmix, drymix, milk):
        IngredientRun(name='{} input'.format(ingredient.name),
                      material=ingredient, process=batter.process)

    wetmix.process = ProcessRun(name='Mixing Wet')
    for ingredient in (sugar, butter, eggs, vanilla):
        IngredientRun(name='{} input'.format(ingredient.name),
                      material=ingredient, process=wetmix.process)

    drymix.process = ProcessRun(name='Mixing Dry')
    for ingredient in (flour, baking_powder, salt):
        IngredientRun(name='{} input'.format(ingredient.name),
                      material=ingredient, process=drymix.process)

    set_uuids(cake)

    frosting.process = ProcessRun(name='Mixing Frosting')
    IngredientRun(name='{} input'.format(butter.name),
                  material=LinkByUID.from_entity(butter), process=frosting.process)
    IngredientRun(name='{} input'.format(chocolate.name),
                  material=chocolate, process=frosting.process)
    IngredientRun(name='{} input'.format(powder_sugar.name),
                  material=powder_sugar, process=frosting.process)
    IngredientRun(name='{} input'.format(vanilla.name),
                  material=LinkByUID.from_entity(vanilla), process=frosting.process)
    IngredientRun(name='{} input'.format(milk.name),
                  material=LinkByUID.from_entity(milk), process=frosting.process)

    frosting_taste = MeasurementRun(name='Frosting Taste', material=frosting)
    frosting_sweetness = MeasurementRun(name='Frosting Sweetness', material=frosting)

    ######################################################################
    # And now let's create abstract cake
    cake.spec = MaterialSpec(name='Abstract Cake')

    baked.spec = MaterialSpec(name='Abstract Baked Cake')
    frosting.spec = MaterialSpec(name='Abstract Frosting')

    batter.spec = MaterialSpec(name='Abstract Batter')

    wetmix.spec = MaterialSpec(name='Abstract Wet Mix')
    drymix.spec = MaterialSpec(name='Abstract Dry Mix')

    flour.spec = MaterialSpec(name='Abstract Flour')
    baking_powder.spec = MaterialSpec(name='Abstract Baking Powder')
    salt.spec = MaterialSpec(name='Abstract Salt')
    sugar.spec = MaterialSpec(name='Abstract Sugar')
    butter.spec = MaterialSpec(name='Abstract Butter')
    eggs.spec = MaterialSpec(name='Abstract Eggs')
    vanilla.spec = MaterialSpec(name='Abstract Vanilla')
    milk.spec = MaterialSpec(name='Abstract Milk')
    chocolate.spec = MaterialSpec(name='Abstract Chocolate')
    powder_sugar.spec = MaterialSpec(name='Abstract Powdered Sugar')

    # with abstract processes
    cake.spec.process = ProcessSpec(name='Icing, in General')
    cake.process.spec = cake.spec.process
    baked.spec.process = ProcessSpec(name='Baking, in General')
    baked.process.spec = baked.spec.process
    batter.spec.process = ProcessSpec(name='Mixing Batter, in General')
    batter.process.spec = batter.spec.process
    wetmix.spec.process = ProcessSpec(name='Mixing Wet, in General')
    wetmix.process.spec = wetmix.spec.process
    drymix.spec.process = ProcessSpec(name='Mixing Dry, in General')
    drymix.process.spec = drymix.spec.process
    frosting.spec.process = ProcessSpec(name='Mixing Frosting, in General')
    frosting.process.spec = frosting.spec.process

    # and abstract ingredients
    for run in cake.process.ingredients:
        run.spec = IngredientSpec(name='{} input'.format(run.material.spec.name),
                                  material=run.material.spec, process=cake.process.spec)

    for run in baked.process.ingredients:
        run.spec = IngredientSpec(name='{} input'.format(run.material.spec.name),
                                  material=run.material.spec, process=baked.process.spec)

    for run in batter.process.ingredients:
        run.spec = IngredientSpec(name='{} input'.format(run.material.spec.name),
                                  material=run.material.spec, process=batter.process.spec)

    for run in wetmix.process.ingredients:
        run.spec = IngredientSpec(name='{} input'.format(run.material.spec.name),
                                  material=run.material.spec, process=wetmix.process.spec)

    for run in drymix.process.ingredients:
        run.spec = IngredientSpec(name='{} input'.format(run.material.spec.name),
                                  material=run.material.spec, process=drymix.process.spec)

    set_uuids(cake)

    for ing_run in frosting.process.ingredients:
        if isinstance(ing_run.material, LinkByUID):
            mat = next(x for x in [butter, vanilla, milk] if x.uids['auto'] == ing_run.material.id)
            ing_run.spec = IngredientSpec(name='{} input'.format(mat.spec.name),
                                          material=LinkByUID.from_entity(mat.spec),
                                          process=frosting.process.spec)
        else:
            ing_run.spec = IngredientSpec(name='{} input'.format(ing_run.material.spec.name),
                                          material=ing_run.material.spec,
                                          process=frosting.process.spec)

    # and spec out the measurements
    cake_taste.spec = MeasurementSpec(name='Taste')
    cake_appearance.spec = MeasurementSpec(name='Appearance')
    frosting_taste.spec = cake_taste.spec  # Taste
    frosting_sweetness.spec = MeasurementSpec(name='Sweetness')

    ######################################################################
    # Let's add some attributes
    baked.process.conditions.append(Condition(name='Cooking time',
                                              template=tmpl['Cooking time'],
                                              origin=Origin.MEASURED,
                                              value=NominalReal(nominal=48, units='min')))
    baked.spec.process.conditions.append(Condition(name='Cooking time',
                                                   template=tmpl['Cooking time'],
                                                   origin=Origin.SPECIFIED,
                                                   value=NormalReal(mean=50, std=5, units='min')))
    baked.process.conditions.append(Condition(name='Oven temperature',
                                              origin="measured",
                                              value=NominalReal(nominal=362, units='degF')))
    baked.spec.process.parameters.append(Parameter(name='Oven temperature setting',
                                                   template=tmpl['Oven temperature setting'],
                                                   origin="specified",
                                                   value=NominalReal(nominal=350, units='degF')))
    cake_taste.properties.append(Property(name='Tastiness',
                                          origin=Origin.MEASURED,
                                          template=tmpl['Tastiness'],
                                          value=NominalInteger(nominal=5)))
    cake_appearance.properties.append(Property(name='Visual Appeal',
                                               origin=Origin.MEASURED,
                                               value=NominalInteger(nominal=5)))
    frosting_taste.properties.append(Property(name='Tastiness',
                                              origin=Origin.MEASURED,
                                              template=tmpl['Tastiness'],
                                              value=NominalInteger(nominal=4)))
    frosting_sweetness.properties.append(Property(name='Sweetness (Sucrose-basis)',
                                                  origin=Origin.MEASURED,
                                                  value=NominalReal(nominal=1.7, units='')))

    baked.process.spec.template = tmpl['Baking in an oven']
    cake_taste.spec.template = tmpl['Taste test']
    frosting_taste.spec.template = tmpl['Taste test']

    cake.spec.template = tmpl['Dessert']
    frosting.spec.template = tmpl['Dessert']

    return cake


if __name__ == "__main__":
    cake = make_cake()
    set_uuids(cake)

    with open("example_taurus_material_history.json", "w") as f:
        context_list = complete_material_history(cake)
        f.write(json.dumps(context_list, indent=2))

    with open("example_taurus_material_template.json", "w") as f:
        f.write(thin_dumps(cake.template, indent=2))

    with open("example_taurus_process_template.json", "w") as f:
        f.write(thin_dumps(cake.process.ingredients[0].material.process.template, indent=2))

    with open("example_taurus_measurement_template.json", "w") as f:
        f.write(thin_dumps(cake.measurements[0].template, indent=2))

    with open("example_taurus_material_spec.json", "w") as f:
        f.write(thin_dumps(cake.spec, indent=2))

    with open("example_taurus_process_spec.json", "w") as f:
        f.write(thin_dumps(cake.process.spec, indent=2))

    with open("example_taurus_ingredient_spec.json", "w") as f:
        f.write(thin_dumps(cake.process.spec.ingredients[0], indent=2))

    with open("example_taurus_measurement_spec.json", "w") as f:
        f.write(thin_dumps(cake.measurements[0].spec, indent=2))

    with open("example_taurus_material_run.json", "w") as f:
        f.write(thin_dumps(cake, indent=2))

    with open("example_taurus_process_run.json", "w") as f:
        f.write(thin_dumps(cake.process, indent=2))

    with open("example_taurus_ingredient_run.json", "w") as f:
        f.write(thin_dumps(cake.process.ingredients[0], indent=2))

    with open("example_taurus_measurement_run.json", "w") as f:
        f.write(thin_dumps(cake.measurements[0], indent=2))

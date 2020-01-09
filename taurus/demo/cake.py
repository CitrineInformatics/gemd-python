"""Bake a cake."""
import json

import random

from taurus.client.json_encoder import thin_dumps
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.parameter import Parameter
from taurus.entity.attribute.property import Property
from taurus.entity.attribute.property_and_conditions import PropertyAndConditions
from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.composition_bounds import CompositionBounds
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
from taurus.entity.value.uniform_integer import UniformInteger
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.value.normal_real import NormalReal
from taurus.entity.value.uniform_real import UniformReal
from taurus.entity.value.nominal_categorical import NominalCategorical
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_composition import NominalComposition
from taurus.entity.value.empirical_formula import EmpiricalFormula
from taurus.enumeration.origin import Origin
from taurus.util.impl import set_uuids
from taurus.entity.util import complete_material_history, make_instance
from taurus.entity.file_link import FileLink
from taurus.entity.source.performed_source import PerformedSource


def make_cake_templates():
    """Define all templates independently, as in the wild this will be an independent operation."""
    tmpl = dict()

    # Attributes
    tmpl['Cooking time'] = ConditionTemplate(
        name="Cooking time",
        description="The time elapsed during a cooking process",
        bounds=RealBounds(0, 7 * 24.0, "hr")
    )
    tmpl["Oven temperature setting"] = ParameterTemplate(
        name="Oven temperature setting",
        description="Where the knob points",
        bounds=RealBounds(0, 2000.0, "K")
    )
    tmpl["Oven temperature"] = ConditionTemplate(
        name="Oven temperature",
        description="Actual temperature measured by the thermocouple",
        bounds=RealBounds(0, 2000.0, "K")
    )

    tmpl["Toothpick test"] = PropertyTemplate(
        name="Toothpick test",
        description="Results of inserting a toothpick to check doneness",
        bounds=CategoricalBounds(["wet", "crumbs", "completely clean"])
    )
    tmpl["Color"] = PropertyTemplate(
        name="Baked color",
        description="Visual observation of the color of a baked good",
        bounds=CategoricalBounds(["Pale", "Golden brown", "Deep brown", "Black"])
    )

    tmpl["Tastiness"] = PropertyTemplate(
        name="Tastiness",
        description="Yumminess on a fairly arbitrary scale",
        bounds=IntegerBounds(lower_bound=1, upper_bound=10)
    )

    tmpl["Nutritional Information"] = PropertyTemplate(
        name="Nutritional Information",
        description="FDA Nutrition Facts, mass basis.  Please be attentive to g vs. mg.  "
                    "`other-carbohydrate` and `other-fat` are the total values minus the "
                    "broken-out quantities. Other is the difference between the total and the "
                    "serving size.",
        bounds=CompositionBounds(
            components=[
                'other',
                'saturated-fat',
                'trans-fat',
                'other-fat',
                'cholesterol',
                'sodium',
                'dietary-fiber',
                'sugars',
                'other-carbohydrate',
                'protein',
                'vitamin-d',
                'calcium',
                'iron',
                'potassium'
            ]
        )
    )
    tmpl["Serving Size"] = ConditionTemplate(
        name="Serving Size",
        description="Serving size in mass units, to go along with FDA Nutrition Facts",
        bounds=RealBounds(1.e-3, 10.e3, "g")
    )

    # Objects
    tmpl["Baking in an oven"] = ProcessTemplate(
        name="Baking in an oven",
        description='Using heat to promote chemical reactions in a material',
        allowed_labels=['precursor'],
        conditions=[(tmpl["Oven temperature"], RealBounds(0, 700, "degF"))],
        parameters=[(tmpl["Oven temperature setting"], RealBounds(100, 550, "degF"))]
    )

    tmpl["Doneness"] = MeasurementTemplate(
        name="Doneness test",
        description="An ensemble of tests to determine the doneness of a baked good",
        properties=[tmpl["Toothpick test"], tmpl["Color"]]
    )

    tmpl["Taste test"] = MeasurementTemplate(
        name="Taste test",
        properties=[tmpl["Tastiness"]]
    )

    tmpl["Dessert"] = MaterialTemplate(
        name="Dessert",
        properties=[tmpl["Tastiness"]]
    )

    tmpl["Generic Material"] = MaterialTemplate(name="Generic")
    tmpl["Nutritional Material"] = MaterialTemplate(
        name="Nutritional Material",
        description="A material with FDA Nutrition Facts attached",
        properties=[
            tmpl["Nutritional Information"]
        ]
    )
    tmpl["Icing"] = ProcessTemplate(name="Icing",
                                    description='Applying a coating to a substrate',
                                    allowed_labels=['coating', 'substrate'])
    tmpl["Mixing"] = ProcessTemplate(name="Mixing",
                                     description='Physically combining ingredients',
                                     allowed_labels=['wet', 'dry', 'leavening', 'seasoning',
                                                     'sweetener', 'shortening', 'flavoring'])
    tmpl["Procurement"] = ProcessTemplate(name="Procurement",
                                          description="Buyin' stuff")

    return tmpl


def make_cake_spec(tmpl=None):
    """Define a recipe for making a cake."""
    ###############################################################################################
    # Templates
    if tmpl is None:
        tmpl = make_cake_templates()

    ###############################################################################################
    # Objects
    cake = MaterialSpec(
        name="Abstract Cake",
        template=tmpl["Dessert"],
        process=ProcessSpec(
            name='Icing, in General',
            template=tmpl["Icing"],
            tags=[
                'spreading'
            ],
            notes='The act of covering a baked output with frosting'
        ),
        properties=[
            PropertyAndConditions(Property(name="Tastiness",
                                           value=NominalInteger(5),
                                           template=tmpl["Tastiness"],
                                           origin="specified"
                                           ))
        ],
        file_links=FileLink(
            filename="Becky's Butter Cake",
            url='https://www.landolakes.com/recipe/16730/becky-s-butter-cake/'
        ),
        tags=[
            'cake::butter cake',
            'dessert::baked::cake',
            'iced::chocolate'
        ],
        notes='Butter cake recipe reminiscent of the 1-2-3-4 cake that Grandma may have baked.'
    )

    ########################
    frosting = MaterialSpec(
        name="Abstract Frosting",
        template=tmpl["Dessert"],
        process=ProcessSpec(
            name='Mixing Frosting, in General',
            template=tmpl["Mixing"],
            tags=[
                'mixing'
            ],
            notes='Combining ingredients to make a sweet frosting'
        ),
        tags=[
            'frosting::chocolate',
            'topping::chocolate'
        ],
        notes='Chocolate frosting'
    )
    IngredientSpec(
        name="{} input".format(frosting.name.replace('Abstract ', '')),
        tags=list(frosting.tags),
        notes='Seems like a lot of frosting',
        labels=['coating'],
        process=cake.process,
        material=frosting,
        absolute_quantity=NominalReal(nominal=0.751, units='kg')
    )

    baked_cake = MaterialSpec(
        name="Abstract Baked Cake",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Baking, in General',
            template=tmpl["Baking in an oven"],
            tags=[
                'oven::baking'
            ],
            notes='Using heat to convert batter into a solid matrix'
        ),
        tags=[
        ],
        notes='The cakey part of the cake'
    )
    IngredientSpec(
        name="{} input".format(baked_cake.name.replace('Abstract ', '')),
        tags=list(baked_cake.tags),
        labels=['substrate'],
        process=cake.process,
        material=baked_cake
    )

    ########################
    batter = MaterialSpec(
        name="Abstract Batter",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Mixing Batter, in General',
            template=tmpl["Mixing"],
            tags=[
                'mixing'
            ],
            notes='Combining ingredients to make a baking feedstock'
        ),
        tags=[
        ],
        notes='The fluid that converts to cake with heat'
    )
    IngredientSpec(
        name="{} input".format(batter.name.replace('Abstract ', '')),
        tags=list(batter.tags),
        labels=['precursor'],
        process=baked_cake.process,
        material=batter
    )

    ########################
    wetmix = MaterialSpec(
        name="Abstract Wet Mix",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Mixing Wet, in General',
            template=tmpl["Mixing"],
            tags=[
                'mixing'
            ],
            notes='Combining wet ingredients to make a baking feedstock'
        ),
        tags=[
        ],
        notes='The wet fraction of a batter'
    )
    IngredientSpec(
        name="{} input".format(wetmix.name.replace('Abstract ', '')),
        tags=list(wetmix.tags),
        labels=['wet'],
        process=batter.process,
        material=wetmix
    )

    drymix = MaterialSpec(
        name="Abstract Dry Mix",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Mixing Dry, in General',
            template=tmpl["Mixing"],
            tags=[
                'mixing'
            ],
            notes='Combining dry ingredients to make a baking feedstock'
        ),
        tags=[
        ],
        notes='The dry fraction of a batter'
    )
    IngredientSpec(
        name="{} input".format(drymix.name.replace('Abstract ', '')),
        tags=list(drymix.tags),
        labels=['dry'],
        process=batter.process,
        material=drymix,
        absolute_quantity=NominalReal(nominal=3.052, units='cups')
    )

    ########################
    flour = MaterialSpec(
        name="Abstract Flour",
        template=tmpl["Nutritional Material"],
        properties=[
            PropertyAndConditions(
                property=Property(
                    name="Nutritional Information",
                    value=NominalComposition(
                        {
                            "dietary-fiber": 1,
                            "sugar": 1,
                            "other-carbohydrate": 20,
                            "protein": 4,
                            "other": 4
                        }
                    ),
                    template=tmpl["Nutritional Information"],
                    origin="specified"
                ),
                conditions=Condition(
                    name="Serving Size",
                    value=NominalReal(30, 'g'),
                    template=tmpl["Serving Size"],
                    origin="specified"
                )
            )
        ],
        process=ProcessSpec(
            name='Buying Flour, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing all purpose flour'
        ),
        tags=[
        ],
        notes='All-purpose flour'
    )
    IngredientSpec(
        name="{} input".format(flour.name.replace('Abstract ', '')),
        tags=list(flour.tags),
        labels=['dry'],
        process=drymix.process,
        material=flour,
        volume_fraction=NominalReal(nominal=0.9829, units='')  # 3 cups
    )

    baking_powder = MaterialSpec(
        name="Abstract Baking Powder",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Baking Powder, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing baking powder'
        ),
        tags=[
        ],
        notes='Leavening agent for cake'
    )
    IngredientSpec(
        name="{} input".format(baking_powder.name.replace('Abstract ', '')),
        tags=list(baking_powder.tags),
        labels=['leavening', 'dry'],
        process=drymix.process,
        material=baking_powder,
        volume_fraction=NominalReal(nominal=0.0137, units='')  # 2 teaspoons
    )

    salt = MaterialSpec(
        name="Abstract Salt",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Salt, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing salt'
        ),
        tags=[
        ],
        notes='Plain old NaCl',
        properties=[
            PropertyAndConditions(Property(name='Formula', value=EmpiricalFormula("NaCl")))
        ]
    )
    IngredientSpec(
        name="{} input".format(salt.name.replace('Abstract ', '')),
        tags=list(salt.tags),
        labels=['dry', 'seasoning'],
        process=drymix.process,
        material=salt,
        volume_fraction=NominalReal(nominal=0.0034, units='')  # 1/2 teaspoon
    )

    sugar = MaterialSpec(
        name="Abstract Sugar",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Sugar, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing all purpose flour'
        ),
        tags=[
        ],
        notes='Sugar',
        properties=[
            PropertyAndConditions(Property(name="Formula", value=EmpiricalFormula("C12H22O11")))
        ]
    )
    IngredientSpec(
        name="{} input".format(sugar.name.replace('Abstract ', '')),
        tags=list(sugar.tags),
        labels=['wet', 'sweetener'],
        process=wetmix.process,
        material=sugar,
        absolute_quantity=NominalReal(nominal=2, units='cups')
    )

    butter = MaterialSpec(
        name="Abstract Butter",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Butter, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::produce'
            ],
            notes='Purchasing butter'
        ),
        tags=[
        ],
        notes='Shortening for making rich, buttery baked goods'
    )
    IngredientSpec(
        name="{} input".format(butter.name.replace('Abstract ', '')),
        tags=list(butter.tags),
        labels=['wet', 'shortening'],
        process=wetmix.process,
        material=butter,
        absolute_quantity=NominalReal(nominal=1, units='cups')
    )
    IngredientSpec(
        name="{} input".format(butter.name.replace('Abstract ', '')),
        tags=list(butter.tags),
        labels=['shortening'],
        process=frosting.process,
        material=butter,
        mass_fraction=NominalReal(nominal=0.1434, units='')  # 1/2 c @ 0.911 g/cc
    )

    eggs = MaterialSpec(
        name="Abstract Eggs",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Eggs, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::produce'
            ],
            notes='Purchasing eggs'
        ),
        tags=[
        ],
        notes=''
    )
    IngredientSpec(
        name="{} input".format(eggs.name.replace('Abstract ', '')),
        tags=list(eggs.tags),
        labels=['wet'],
        process=wetmix.process,
        material=eggs,
        absolute_quantity=NominalReal(nominal=4, units='')
    )

    vanilla = MaterialSpec(
        name="Abstract Vanilla",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Vanilla, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing vanilla'
        ),
        tags=[
        ],
        notes=''
    )
    IngredientSpec(
        name="{} input".format(vanilla.name.replace('Abstract ', '')),
        tags=list(vanilla.tags),
        labels=['wet', 'flavoring'],
        process=wetmix.process,
        material=vanilla,
        absolute_quantity=NominalReal(nominal=2, units='teaspoons')
    )
    IngredientSpec(
        name="{} input".format(vanilla.name.replace('Abstract ', '')),
        tags=list(vanilla.tags),
        labels=['flavoring'],
        process=frosting.process,
        material=vanilla,
        mass_fraction=NominalReal(nominal=0.0231, units='')  # 2 tsp @ 0.879 g/cc
    )

    milk = MaterialSpec(
        name="Abstract Milk",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Milk, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::produce'
            ],
            notes='Purchasing milk'
        ),
        tags=[
        ],
        notes=''
    )
    IngredientSpec(
        name="{} input".format(milk.name.replace('Abstract ', '')),
        tags=list(milk.tags),
        labels=['wet'],
        process=batter.process,
        material=milk,
        absolute_quantity=NominalReal(nominal=1, units='cup')
    )
    IngredientSpec(
        name="{} input".format(milk.name.replace('Abstract ', '')),
        tags=list(milk.tags),
        labels=[],
        process=frosting.process,
        material=milk,
        mass_fraction=NominalReal(nominal=0.0816, units='')  # 1/4 c @ 1.037 g/cc
    )

    chocolate = MaterialSpec(
        name="Abstract Chocolate",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Chocolate, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing chocolate'
        ),
        tags=[
        ],
        notes=''
    )
    IngredientSpec(
        name="{} input".format(chocolate.name.replace('Abstract ', '')),
        tags=list(chocolate.tags),
        labels=['flavoring'],
        process=frosting.process,
        material=chocolate,
        mass_fraction=NominalReal(nominal=0.1132, units='')  # 3 oz.
    )

    powder_sugar = MaterialSpec(
        name="Abstract Powdered Sugar",
        template=tmpl["Generic Material"],
        process=ProcessSpec(
            name='Buying Powdered Sugar, in General',
            template=tmpl["Procurement"],
            tags=[
                'purchase::dry-goods'
            ],
            notes='Purchasing powdered sugar'
        ),
        tags=[
        ],
        notes='Granulated sugar mixed with corn starch'
    )
    IngredientSpec(
        name="{} input".format(powder_sugar.name.replace('Abstract ', '')),
        tags=list(powder_sugar.tags),
        labels=['flavoring'],
        process=frosting.process,
        material=powder_sugar,
        mass_fraction=NominalReal(nominal=0.6387, units='')  # 4 c @ 30 g/ 0.25 cups
    )
    return cake


def make_cake(seed=None, tmpl=None, cake_spec=None):
    """Define all objects that go into making a demo cake."""
    if seed is not None:
        random.seed(seed)
    ######################################################################
    # Parent Objects
    if tmpl is None:
        tmpl = make_cake_templates()
    if cake_spec is None:
        cake_spec = make_cake_spec(tmpl)

    ######################################################################
    # Objects
    cake = make_instance(cake_spec)
    operators = ['gwash', 'jadams', 'thomasj', 'jmadison', 'jmonroe']
    cake.process.source = PerformedSource(performed_by=random.choice(operators),
                                          performed_date='2015-03-14')
    # Replace Abstract/In General
    queue = [cake]
    while queue:
        item = queue.pop(0)
        item.name = item.name.replace('Abstract ', '').replace(', in General', '')
        if item.spec.tags is not None:
            item.tags = list(item.spec.tags)
        if item.spec.notes:  # None or empty string
            item.notes = 'The spec says "{}"'.format(item.spec.notes)

        if isinstance(item, MaterialRun):
            queue.append(item.process)
        elif isinstance(item, ProcessRun):
            queue.extend(item.ingredients)
            if item.template.name == "Procurement":
                item.source = PerformedSource(performed_by='hamilton',
                                              performed_date='2015-02-17')
            else:
                item.source = cake.process.source
        elif isinstance(item, IngredientRun):
            queue.append(item.material)
            fuzz = 0.95 + 0.1 * random.random()
            if item.spec.absolute_quantity is not None:
                item.absolute_quantity = \
                    NormalReal(mean=fuzz * item.spec.absolute_quantity.nominal,
                               std=0.05 * item.spec.absolute_quantity.nominal,
                               units=item.spec.absolute_quantity.units)
            if item.spec.volume_fraction is not None:
                item.volume_fraction = \
                    NormalReal(mean=fuzz * item.spec.volume_fraction.nominal,
                               std=0.05 * item.spec.volume_fraction.nominal,
                               units=item.spec.volume_fraction.units)
            if item.spec.mass_fraction is not None:
                item.mass_fraction = \
                    UniformReal(lower_bound=(fuzz - 0.05) * item.spec.mass_fraction.nominal,
                                upper_bound=(fuzz + 0.05) * item.spec.mass_fraction.nominal,
                                units=item.spec.mass_fraction.units)
            if item.spec.number_fraction is not None:
                item.number_fraction = \
                    NormalReal(mean=fuzz * item.spec.number_fraction.nominal,
                               std=0.05 * item.spec.number_fraction.nominal,
                               units=item.spec.number_fraction.units)

        else:
            raise TypeError("Unexpected object in the queue")

    frosting = \
        next(x.material for x in cake.process.ingredients if 'rosting' in x.name)
    baked = \
        next(x.material for x in cake.process.ingredients if 'aked' in x.name)

    # Add measurements
    cake_taste = MeasurementRun(name='Final Taste', material=cake)
    cake_appearance = MeasurementRun(name='Final Appearance', material=cake)
    frosting_taste = MeasurementRun(name='Frosting Taste', material=frosting)
    frosting_sweetness = MeasurementRun(name='Frosting Sweetness', material=frosting)
    baked_doneness = MeasurementRun(name='Baking doneness', material=baked)

    # and spec out the measurements
    cake_taste.spec = MeasurementSpec(name='Taste', template=tmpl['Taste test'])
    cake_appearance.spec = MeasurementSpec(name='Appearance')
    frosting_taste.spec = cake_taste.spec  # Taste
    frosting_sweetness.spec = MeasurementSpec(name='Sweetness')
    baked_doneness.spec = MeasurementSpec(name='Sweetness', template=tmpl["Doneness"])

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
                                          value=UniformInteger(4, 5)))
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

    baked_doneness.properties.append(Property(
        name='Toothpick test',
        origin="measured",
        template=tmpl["Toothpick test"],
        value=NominalCategorical("crumbs")
    ))
    baked_doneness.properties.append(Property(
        name='Color',
        origin="measured",
        template=tmpl["Color"],
        value=DiscreteCategorical({
            "Pale": 0.05,
            "Golden brown": 0.65,
            "Deep brown": 0.3
        })
    ))

    baked.process.spec.template = tmpl['Baking in an oven']
    cake_taste.spec.template = tmpl['Taste test']
    frosting_taste.spec.template = tmpl['Taste test']

    cake.spec.template = tmpl['Dessert']
    frosting.spec.template = tmpl['Dessert']

    # Code to force all scopes to 'id'
    set_uuids([cake, cake_taste, cake_appearance, frosting_taste, frosting_sweetness], name='id')
    id_queue = [x for x in cake.process.ingredients]
    while id_queue:
        x = id_queue.pop(0)
        set_uuids([x], name='id')
        id_queue += x.material.process.ingredients

    return cake


if __name__ == "__main__":
    cake = make_cake(seed=42)

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

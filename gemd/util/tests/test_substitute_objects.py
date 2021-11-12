from gemd.util import substitute_objects, recursive_foreach, flatten, make_index, recursive_flatmap
from gemd.util.impl import _substitute, _substitute_inplace
from gemd.entity.object import MaterialSpec, MaterialRun, ProcessSpec, ProcessRun, IngredientRun, \
    IngredientSpec, MeasurementSpec
from gemd.entity.template import ProcessTemplate, ParameterTemplate, MeasurementTemplate
from gemd.entity.value.normal_real import NormalReal
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.bounds.real_bounds import RealBounds


def test_dictionary_substitution():
    """substitute_objects() should substitute LinkByUIDs that occur in dict keys and values."""
    proc = ProcessRun("A process", uids={'id': '123'})
    mat = MaterialRun("A material", uids={'generic id': '38f8jf'})

    proc_link = LinkByUID.from_entity(proc)
    mat_link = LinkByUID.from_entity(mat)
    index = {(mat_link.scope.lower(), mat_link.id): mat,
             (proc_link.scope.lower(), proc_link.id): proc}

    test_dict = {LinkByUID.from_entity(proc): LinkByUID.from_entity(mat)}
    subbed = substitute_objects(test_dict, index)
    k, v = next((k, v) for k, v in subbed.items())
    assert k == proc
    assert v == mat


def test_tuple_sub():
    """substitute_objects() should correctly substitute tuple values."""
    proc = ProcessRun('foo', uids={'id': '123'})
    proc_link = LinkByUID.from_entity(proc)
    index = {(proc_link.scope, proc_link.id): proc}
    tup = (proc_link,)
    subbed = substitute_objects(tup, index)
    assert subbed[0] == proc


def test_recursive_foreach():
    """Test that recursive_foreach() applies a method to every object."""
    new_tag = "Extra tag"

    def func(base_ent):
        """Adds a specific tag to the object."""
        base_ent.tags.extend([new_tag])
        return

    param_template = ParameterTemplate("a param template", bounds=RealBounds(0, 100, ''))
    meas_template = MeasurementTemplate("Measurement template", parameters=[param_template])
    parameter = Parameter(name="A parameter", value=NormalReal(mean=17, std=1, units=''))
    measurement = MeasurementSpec(name="name", parameters=parameter, template=meas_template)
    test_dict = {"foo": measurement}
    recursive_foreach(test_dict, func, apply_first=True)

    for ent in [param_template, meas_template, measurement]:
        assert new_tag in ent.tags


def test_substitute_equivalence():
    """PLA-6423: verify that substitutions match up."""
    spec = ProcessSpec(name="old spec", uids={'scope': 'spec'})
    run = ProcessRun(name="old run",
                     uids={'scope': 'run'},
                     spec=LinkByUID(id='spec', scope="scope"))

    # make a dictionary from ids to objects, to be used in substitute_objects
    gem_index = make_index([run, spec])
    substitute_objects(obj=run, index=gem_index, inplace=True)
    assert spec == run.spec


def test_complex_substitutions():
    """Make sure accounting works for realistic objects."""
    root = MaterialRun("root",
                       process=ProcessRun("root", spec=ProcessSpec("root")),
                       spec=MaterialSpec("root")
                       )
    root.spec.process = root.process.spec
    input = MaterialRun("input",
                        process=ProcessRun("input", spec=ProcessSpec("input")),
                        spec=MaterialSpec("input")
                        )
    input.spec.process = input.process.spec
    IngredientRun(process=root.process,
                  material=input,
                  spec=IngredientSpec("ingredient",
                                      process=root.process.spec,
                                      material=input.spec
                                      )
                  )
    param = ParameterTemplate("Param", bounds=RealBounds(-1, 1, "m"))
    root.process.spec.template = ProcessTemplate("Proc",
                                                 parameters=[param]
                                                 )
    root.process.parameters.append(Parameter("Param",
                                             value=NormalReal(0, 1, 'm'),
                                             template=param))

    links = flatten(root, scope="test-scope")
    index = make_index(links)
    rebuild = substitute_objects(links, index, inplace=True)
    rebuilt_root = next(x for x in rebuild if x.name == root.name and x.typ == root.typ)
    all_objs = recursive_flatmap(rebuilt_root,
                                 func=lambda x: [x],
                                 unidirectional=False
                                 )
    unique = [x for i, x in enumerate(all_objs) if i == all_objs.index(x)]
    assert not any(isinstance(x, LinkByUID) for x in unique), "All are objects"
    assert len(links) == len(unique), "Objects are missing"


def test_sub_inplace_lists():
    """Verify consistency for nested lists."""
    lst_one = [1, 2, 3]
    lol_main = [
        lst_one,
        [
            [1, 2, 3],
        ],
        lst_one
    ]
    lol_dup = _substitute(lol_main,
                          applies=lambda x: isinstance(x, int),
                          sub=lambda x: x + 1)
    assert lol_dup != lol_main

    lol_mod = _substitute_inplace(lol_main,
                                  applies=lambda x: isinstance(x, int),
                                  sub=lambda x: x + 1)
    assert lol_mod == lol_main
    assert lol_mod == lol_dup


def test_sub_inplace_tuples():
    """Verify consistency for nested tuples."""
    lot_main = [  # Base object must mutable to make sense for inplace
        (1, 2, 3),
        (
            (1, 2, 3),
        ),
        (1, 2, 3)
    ]
    lot_dup = _substitute(lot_main,
                          applies=lambda x: isinstance(x, int),
                          sub=lambda x: x + 1)
    assert lot_dup != lot_main

    lot_mod = _substitute_inplace(lot_main,
                                  applies=lambda x: isinstance(x, int),
                                  sub=lambda x: x + 1)
    assert lot_mod == lot_main
    assert lot_mod == lot_dup


def test_sub_inplace_dicts():
    """Verify consistency for nested dicts."""
    dod_main = {
        1: 1,
        "sub": {1: 1, 2: 2, 3: 3},
        3: 3,
    }
    dod_dup = _substitute(dod_main,
                          applies=lambda x: isinstance(x, int),
                          sub=lambda x: x + 1)
    assert dod_dup != dod_main

    dod_mod = _substitute_inplace(dod_main,
                                  applies=lambda x: isinstance(x, int),
                                  sub=lambda x: x + 1)
    assert dod_mod == dod_main
    assert dod_mod == dod_dup

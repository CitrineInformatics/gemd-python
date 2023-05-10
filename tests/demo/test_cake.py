"""Test cake demo."""
from gemd.entity.object.material_spec import MaterialSpec
from gemd.entity.object.material_run import MaterialRun
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.object.process_spec import ProcessSpec
from gemd.entity.object.measurement_spec import MeasurementSpec
from gemd.entity.object.measurement_run import MeasurementRun
from gemd.entity.object.ingredient_spec import IngredientSpec
from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.file_link import FileLink

from gemd.json import dumps, loads
from gemd.demo.cake import make_cake_templates, make_cake_spec, make_cake, \
    import_toothpick_picture, change_scope, get_demo_scope, get_template_scope
from gemd.util import recursive_foreach


def test_cake():
    """Create cake, serialize, deserialize."""
    cake = make_cake(seed=42)

    # Check that all the objects show up
    tot_count = 0

    def increment(dummy):
        nonlocal tot_count
        tot_count += 1

    recursive_foreach(cake, increment)
    assert tot_count == 139

    # Check that no UIDs collide
    uid_seen = dict()

    def _check_ids(obj):
        nonlocal uid_seen
        for scope in obj.uids:
            lbl = '{}::{}'.format(scope, obj.uids[scope].lower())
            if lbl in uid_seen:
                assert uid_seen[lbl] == id(obj), "'{}' seen twice".format(lbl)
            uid_seen[lbl] = id(obj)
    recursive_foreach(cake, _check_ids)

    # Check that all recursive and square links are structured correctly
    def _check_crosslinks(obj):
        if isinstance(obj, MaterialSpec):
            assert obj.process.output_material == obj
        elif isinstance(obj, MaterialRun):
            assert obj.process.output_material == obj
            for msr in obj.measurements:
                assert msr.material == obj
            assert obj.spec.process == obj.process.spec
        elif isinstance(obj, ProcessRun):
            assert obj.output_material.process == obj
            assert obj.spec.output_material == obj.output_material.spec
        elif isinstance(obj, ProcessSpec):
            assert obj.output_material.process == obj
        elif isinstance(obj, MeasurementSpec):
            pass  # Doesn't link
        elif isinstance(obj, MeasurementRun):
            assert obj in obj.material.measurements
        elif isinstance(obj, IngredientSpec):
            assert obj in obj.process.ingredients
        elif isinstance(obj, IngredientRun):
            assert obj in obj.process.ingredients
            assert obj.spec.material == obj.material.spec
    recursive_foreach(cake, _check_crosslinks)


def test_cake_sigs():
    """Verify that all arguments for create methods work as expected."""
    templates = make_cake_templates()
    tmpl_snap = dumps(templates)

    specs = make_cake_spec(templates)
    spec_snap = dumps(specs)
    assert dumps(templates) == tmpl_snap

    cake1 = make_cake(seed=27, cake_spec=specs, tmpl=templates)
    assert dumps(templates) == tmpl_snap
    assert dumps(specs) == spec_snap

    filelink = FileLink(filename='The name of the file', url='www.file.gov')
    cake2 = make_cake(seed=27, cake_spec=specs, tmpl=templates, toothpick_img=filelink)

    assert filelink.filename not in dumps(cake1)
    assert filelink.filename in dumps(cake2)
    assert cake1.uids == cake2.uids


def test_import():
    """Make sure picture import runs."""
    import_toothpick_picture()


def test_scope():
    """Make sure change scope does what we want it to."""
    default_cake = make_cake()
    default_scope = next(iter(default_cake.uids))

    change_scope('second-scope')
    second_cake = make_cake()

    change_scope(data='third-scope', templates='also-a-scope')
    assert get_demo_scope() == 'third-scope'
    assert get_template_scope() == 'also-a-scope'
    third_cake = make_cake()

    assert 'second-scope' not in default_cake.uids
    assert 'third-scope' not in default_cake.uids

    assert default_scope not in second_cake.uids
    assert 'second-scope' in second_cake.uids
    assert 'third-scope' not in second_cake.uids

    assert default_scope not in third_cake.uids
    assert 'second-scope' not in third_cake.uids
    assert 'third-scope' in third_cake.uids

    assert any('template' in x for x in default_cake.spec.template.uids)
    assert not any('template' in x for x in third_cake.spec.template.uids)


def test_recursive_equals():
    """Verify that the recursive/crawling equals behaves well."""
    cake = make_cake()
    copy = loads(dumps(cake))
    assert cake == copy

    copy.process.ingredients[0].material.process.ingredients[0].material.tags.append('Hi')
    assert cake != copy

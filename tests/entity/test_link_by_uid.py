"""General tests of LinkByUID dynamics."""
import pytest

from gemd.json import dumps, loads
from gemd.entity.object import MaterialRun, ProcessRun, IngredientRun
from gemd.entity.link_by_uid import LinkByUID


def test_link_by_uid():
    """Test that linking works."""
    root = MaterialRun(name='root', process=ProcessRun(name='root proc'))
    leaf = MaterialRun(name='leaf', process=ProcessRun(name='leaf proc'))
    IngredientRun(process=root.process, material=leaf)
    IngredientRun(process=root.process, material=LinkByUID.from_entity(leaf, scope='id'))

    # Paranoid assertions about equality's symmetry since it's implemented in 2 places
    assert root.process.ingredients[0].material == root.process.ingredients[1].material
    assert root.process.ingredients[0].material.__eq__(root.process.ingredients[1].material)
    assert root.process.ingredients[1].material.__eq__(root.process.ingredients[0].material)

    # Verify hash collision on equal LinkByUIDs
    assert LinkByUID.from_entity(leaf) in {LinkByUID.from_entity(leaf)}

    copy = loads(dumps(root))
    assert copy.process.ingredients[0].material == copy.process.ingredients[1].material


def test_from_entity():
    """Test permutations of LinkByUID.from_entity arguments."""
    run = MaterialRun(name='leaf', process=ProcessRun(name='leaf proc'))
    assert LinkByUID.from_entity(run).scope == 'auto'
    assert LinkByUID.from_entity(run, scope='missing').scope == 'auto'
    assert len(run.uids) == 1

    run.uids['foo'] = 'bar'
    link1 = LinkByUID.from_entity(run, scope='foo')
    assert (link1.scope, link1.id) == ('foo', 'bar')


def test_equality():
    """Test that the __eq__ method performs as expected."""
    link = LinkByUID(scope="foo", id="bar")
    assert link == ProcessRun("Good", uids={"foo": "bar"})
    assert link != ProcessRun("Good", uids={"foo": "rab"})
    assert link != ProcessRun("Good", uids={"oof": "bar"})
    assert link != LinkByUID(scope="foo", id="rab")
    assert link == ("foo", "bar")
    assert link != ("foo", "bar", "baz")
    assert link != ("foo", "rab")
    assert link != "foo: rab"

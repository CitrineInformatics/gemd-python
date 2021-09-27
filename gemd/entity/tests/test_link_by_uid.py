"""General tests of LinkByUID dynamics."""
from gemd.json import dumps, loads
from gemd.entity.object.material_run import MaterialRun
from gemd.entity.object.process_run import ProcessRun
from gemd.entity.object.ingredient_run import IngredientRun
from gemd.entity.link_by_uid import LinkByUID


def test_link_by_uid():
    """Test that linking works."""
    root = MaterialRun(name='root', process=ProcessRun(name='root proc'))
    leaf = MaterialRun(name='leaf', process=ProcessRun(name='leaf proc'))
    IngredientRun(process=root.process, material=leaf)
    IngredientRun(process=root.process, material=LinkByUID.from_entity(leaf))

    # Paranoid assertions about equality's symmetry since it's implemented in 2 places
    assert root.process.ingredients[0].material == root.process.ingredients[1].material
    assert root.process.ingredients[0].material.__eq__(root.process.ingredients[1].material)
    assert root.process.ingredients[1].material.__eq__(root.process.ingredients[0].material)

    # Verify hash collision on equal LinkByUIDs
    assert LinkByUID.from_entity(leaf) in {LinkByUID.from_entity(leaf)}

    copy = loads(dumps(root))
    assert copy.process.ingredients[0].material == copy.process.ingredients[1].material

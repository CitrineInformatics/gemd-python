"""General tests of LinkByUID dynamics."""
from taurus.json import dumps, loads
from taurus.entity.object.material_run import MaterialRun
from taurus.entity.object.process_run import ProcessRun
from taurus.entity.object.ingredient_run import IngredientRun
from taurus.entity.link_by_uid import LinkByUID


def test_link_by_uid():
    """Test that linking works."""
    root = MaterialRun(name='root', process=ProcessRun(name='root proc'))
    leaf = MaterialRun(name='leaf', process=ProcessRun(name='leaf proc'))
    IngredientRun(process=root.process, material=leaf)
    IngredientRun(process=root.process, material=LinkByUID.from_entity(leaf))

    copy = loads(dumps(root))
    assert copy.process.ingredients[0].material == copy.process.ingredients[1].material

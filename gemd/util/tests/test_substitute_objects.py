from gemd.util.impl import substitute_objects, recursive_foreach
from gemd.entity.object import ProcessRun, MaterialRun, MeasurementSpec
from gemd.entity.value.normal_real import NormalReal
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.template.parameter_template import ParameterTemplate
from gemd.entity.template.measurement_template import MeasurementTemplate
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.bounds.real_bounds import RealBounds


def test_dictionary_substitution():
    """substitute_objects() should substitute LinkByUIDs that occur in dict keys and values."""
    proc = ProcessRun("A process", uids={"id": "123"})
    mat = MaterialRun("A material", uids={"generic id": "38f8jf"})

    proc_link = LinkByUID.from_entity(proc)
    mat_link = LinkByUID.from_entity(mat)
    index = {
        (mat_link.scope.lower(), mat_link.id): mat,
        (proc_link.scope.lower(), proc_link.id): proc,
    }

    test_dict = {LinkByUID.from_entity(proc): LinkByUID.from_entity(mat)}
    subbed = substitute_objects(test_dict, index)
    k, v = next((k, v) for k, v in subbed.items())
    assert k == proc
    assert v == mat


def test_tuple_sub():
    """substitute_objects() should correctly substitute tuple values."""
    proc = ProcessRun("foo", uids={"id": "123"})
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

    param_template = ParameterTemplate(
        "a param template", bounds=RealBounds(0, 100, "")
    )
    meas_template = MeasurementTemplate(
        "Measurement template", parameters=[param_template]
    )
    parameter = Parameter(
        name="A parameter", value=NormalReal(mean=17, std=1, units="")
    )
    measurement = MeasurementSpec(
        name="name", parameters=parameter, template=meas_template
    )
    test_dict = {"foo": measurement}
    recursive_foreach(test_dict, func, apply_first=True)

    for ent in [param_template, meas_template, measurement]:
        assert new_tag in ent.tags

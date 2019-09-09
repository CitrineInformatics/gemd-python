"""Tests of process templates."""
import pytest

from taurus.client.json_encoder import copy, loads, dumps
from taurus.entity.attribute.condition import Condition
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.integer_bounds import IntegerBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.link_by_uid import LinkByUID
from taurus.entity.object import ProcessSpec, ProcessRun
from taurus.entity.template.condition_template import ConditionTemplate
from taurus.entity.template.parameter_template import ParameterTemplate
from taurus.entity.template.process_template import ProcessTemplate
from taurus.entity.value.discrete_categorical import DiscreteCategorical
from taurus.entity.value.nominal_real import NominalReal

condition_template = ConditionTemplate(
    name="cond",
    bounds=RealBounds(lower_bound=0.0, upper_bound=1.0, default_units='')
)
cat_template = ConditionTemplate(
    name="options",
    bounds=CategoricalBounds(categories={"salt", "not_salt"})
)
parameter_template = ParameterTemplate(
    name="setting",
    bounds=IntegerBounds(0, 101)
)
process_template = ProcessTemplate(
    name="proc",
    conditions=[
        (condition_template, RealBounds(lower_bound=0.5, upper_bound=1.0, default_units='')),
        (cat_template, CategoricalBounds(categories={"salt"})),
    ],
    parameters=[(parameter_template, IntegerBounds(0, 11))]
)


def test_json():
    """Test that serde of a process template preserves its structure."""
    assert loads(dumps(process_template)) == process_template


def test_valid():
    """Test some valid template assignments."""
    ProcessSpec(
        conditions=Condition(name="cond", value=NominalReal(0.5, '')),
        template=process_template
    )

    ProcessSpec(
        conditions=Condition(name="cond", value=NominalReal(0.5, ''))
    ).template = process_template

    ProcessSpec(
        conditions=Condition(name="cond", value=NominalReal(0.5, ''), template=condition_template),
        template=process_template
    )

    ProcessSpec(
        conditions=Condition(name="another_cond", value=NominalReal(1.5, '')),
        template=process_template
    )

    ProcessSpec(
        conditions=Condition(name="cond", value=NominalReal(1, ''), template=condition_template),
        template=process_template
    )

    ProcessSpec(
        conditions=[
            Condition(name="cond", value=NominalReal(1, '')),
            Condition(name="options", value=DiscreteCategorical("salt"), template=cat_template)
        ],
        template=process_template
    )


def test_run_spec_template_equality():
    """Test that assigning a spec to a run causes the run to get the spec's template."""
    spec = ProcessSpec(
        conditions=Condition(name="cond", value=NominalReal(1, ''), template=condition_template),
        template=process_template
    )
    run = ProcessRun(spec=spec)
    assert run.template == spec.template
    # if the run has no spec, then it has no template
    run.spec = None
    assert run.template is None
    # A LinkByUID should be a valid template for both spec and run
    spec.template = LinkByUID(scope="custom template id", id="1234567")
    run.spec = spec
    assert run.template == spec.template
    # if the spec is a LinkByUID, then we don't know its template, so the run gets no template
    run.spec = LinkByUID(scope="custom spec id", id="aaaaaaaaaa")
    assert run.template is None


def test_attribute_template_equality():
    """Test valid template assignments that rely on content equality."""
    ProcessSpec(
        conditions=Condition("cond", value=NominalReal(1, ''), template=copy(condition_template)),
        template=process_template
    )


def test_invalid():
    """Test some invalid template assignments."""
    with pytest.raises(RuntimeWarning):
        ProcessSpec(
            conditions=Condition(name="cond", value=NominalReal(1.5, '')),
            template=process_template
        )

    with pytest.raises(RuntimeWarning):
        ProcessSpec(
            conditions=Condition(name="cond", value=NominalReal(0.25, '')),
            template=process_template
        )

    with pytest.raises(RuntimeWarning):
        ProcessSpec(
            conditions=Condition(name="cond", value=NominalReal(0.25, ''))
        ).template = process_template

    with pytest.raises(ValueError):
        another_template = ConditionTemplate(
            name="cond",
            bounds=RealBounds(lower_bound=0.2, upper_bound=0.8, default_units='')
        )
        ProcessSpec(
            conditions=Condition("cond", value=NominalReal(0.75, ''), template=another_template),
            template=process_template
        )

    with pytest.raises(RuntimeWarning):
        ProcessSpec(
            conditions=[
                Condition(name="cond", value=NominalReal(1, '')),  # int (1) is not a float
                Condition(name="options", value=DiscreteCategorical("not_salt"))
            ],
            template=process_template
        )


def test_homogenize_link():
    """Test behavior when the attribute templates have links in them."""
    link = LinkByUID(scope="foo", id="bar")
    bounds = RealBounds(lower_bound=0, upper_bound=1, default_units="")

    # if we provide the bounds, then we can defer the consistency check with the template
    # to when we write to a data service
    ProcessTemplate(
        name="spam",
        conditions=[(link, bounds)]
    )

    # if we don't provide the bounds, then we can't pull the default bounds out of the link
    # and are stuck.  This is an expression of conditions=[list of attributes] is really just
    # sugar.  The "proper" thing is to provide the bounds explicitly.
    with pytest.raises(TypeError):
        ProcessTemplate(
            name="eggs",
            conditions=[link]
        )

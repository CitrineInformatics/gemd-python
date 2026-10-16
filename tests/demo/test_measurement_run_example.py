"""Test measurement demo."""

from gemd.demo.measurement_example import make_demo_measurements
from gemd.json import dumps, loads


def test_measurement_example(tmp_path):
    """Simple driver to populate flex_measurements.json and validate that it has contents."""
    num_measurements = 4
    results = make_demo_measurements(num_measurements, extra_tags={"demo"})

    filename = tmp_path / "flex_measurements.json"
    filename.write_text(dumps(results, indent=2))
    copy = loads(filename.read_text())

    assert len(copy) == len(results)
    assert all("demo" in x.tags for x in copy)
    assert all("my_id" in x.uids for x in copy)

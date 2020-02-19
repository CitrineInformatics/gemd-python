"""Test measurement demo."""
from taurus.json import dumps, load
from taurus.demo.measurement_example import make_demo_measurements


def test_measurement_example():
    """Simple driver to populate flex_measurements.json and validate that it has contents."""
    num_measurements = 4
    results = make_demo_measurements(num_measurements, extra_tags={"demo"})

    with open("flex_measurements.json", "w") as f:
        f.write(dumps(results, indent=2))

    with open("flex_measurements.json", "r") as f:
        copy = load(f)

    assert len(copy) == len(results)
    assert all("demo" in x.tags for x in copy)
    assert all("my_id" in x.uids for x in copy)

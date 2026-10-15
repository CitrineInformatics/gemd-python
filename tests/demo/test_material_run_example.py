"""Test the ingestion of a material run."""

from gemd.demo.material_run_example import ingest_material_run
from gemd.json import dumps, loads

# Example data (that could have been loaded from a json file)
example = {
    "sample_id": "37e6b61f-b55c-43f1-a14d-534fc29c86f8",
    "tags": ["example", "demo", "json"],
    "experiments": [
        {
            "knob_2_setting": "low",
            "temperature": "300 degF",
            "density": "1.0 +- 0.5 g/cm^3",
            "tags": "warm up",
        },
        {
            "knob_2_setting": "low",
            "temperature": "302 degF",
            "density": "1.04 +- 0.1 g/cm^3",
            "tags": ["high quality", "hutch"],
        },
        {"knob_2_setting": "medium", "density": "0.9 +- 0.4 g/cm^3", "tags": ["oops"]},
        {
            "knob_2_setting": "medium",
            "temperature": "456 degF",
            "density": "0.87 +- 0.1 g/cm^3",
            "tags": ["high quality", "hutch"],
        },
        {
            "knob_2_setting": "high",
            "temperature": "624 degF",
            "density": "0.80 +- 0.12 g/cm^3",
            "kinematic viscosity": "0.1 m^2/s",
            "tags": ["hutch", "viscous"],
        },
    ],
}


def test_example(tmp_path):
    """Test the ingest of a material run and leave evidence for humans."""
    # run the parsing to make sure no exceptions are thrown
    result = ingest_material_run(example)
    filename = tmp_path / "material_run_example.json"

    assert len(result.measurements) == len(example["experiments"])

    # write to a file (for human inspection)
    filename.write_text(dumps(result, indent=2))

    # read it back
    copy = loads(filename.read_text())

    # very cursory check that we get out what we'd expect
    assert next(iter(copy.uids.values())) == example["sample_id"]

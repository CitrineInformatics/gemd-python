"""Test an example table."""
import pandas as pd

from gemd.json import load, dump
from gemd.entity.object import MaterialRun
from gemd.demo.table_example import ingest_table


data = [
    {"vapor pressure": 2.0, "temperature": 300},
    {"vapor pressure": 3.0, "temperature": 400},
]


def test_table(tmp_path):
    """Convert a dictionary to a pandas dataframe and then to a table."""
    material = MaterialRun("name")
    df = pd.DataFrame.from_records(data)
    result = ingest_table(material, df)
    assert isinstance(result, MaterialRun)
    assert len(result.measurements) == len(data)

    filename = tmp_path / "table_example.json"

    # write to a file (for human inspection)
    with open(filename, "w") as f:
        dump(result, f, indent=2)

    # read it back
    with open(filename, "r") as f:
        copy = load(f)

    assert isinstance(copy, MaterialRun)

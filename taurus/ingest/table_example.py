"""Ingest a table."""
from taurus.entity.attribute.condition import Condition
from taurus.entity.attribute.property import Property
from taurus.entity.object import MeasurementRun
from taurus.entity.value.nominal_real import NominalReal

known_properties = ["vapor pressure"]
known_conditions = ["temperature"]


def ingest_table(material_run, table):
    """Ingest a material run into an existing table."""
    for _, row in table.iterrows():
        exp = MeasurementRun()
        for prop_name in known_properties:
            if prop_name in row:
                exp.properties.append(Property(name=prop_name,
                                               value=NominalReal(row[prop_name], '')))
        for cond_name in known_conditions:
            if cond_name in row:
                exp.conditions.append(Condition(name=cond_name,
                                                value=NominalReal(row[cond_name], '')))
        exp.material = material_run

    return material_run

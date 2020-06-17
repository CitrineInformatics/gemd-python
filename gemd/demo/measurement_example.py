"""Demonstrate attaching measurements to a material."""
import random
import string

from gemd.entity.attribute.property import Property
from gemd.entity.object import MeasurementRun
from gemd.entity.value.nominal_real import NominalReal
from gemd.entity.value.normal_real import NormalReal
from gemd.enumeration import Origin

# recommended values taken from
# https://www.shimadzu.com/an/industry/petrochemicalchemical/n9j25k00000pyv3w.html
thickness = 4.0  # mm
length = 80.0  # mm
width = 10.0  # mm
span = 64.0  # mm
punch_radius = 5.0  # mm
support_radius = 5.0  # mm
applied_force = 100.0  # N


def __random_my_id():
    """Create random 8-letter id."""
    return "".join([random.choice(string.ascii_lowercase) for _ in range(8)])


def make_demo_measurements(num_measurements, extra_tags=frozenset()):
    """Make a measurement object."""
    return [
        make_flexural_test_measurement(
            my_id=__random_my_id(),
            deflection=random.random(),
            extra_tags=extra_tags
        ) for _ in range(num_measurements)
    ]


def make_flexural_test_measurement(my_id, deflection, extra_tags=frozenset()):
    """
    Compute the stree, strain, and modulus.

    According to https://en.wikipedia.org/wiki/Three-point_flexural_test
    """
    stress = 3 * applied_force * span / (2 * thickness * thickness * width)
    strain = 6 * deflection * thickness / (span * span)
    modulus = stress / strain

    measurement = MeasurementRun(
        name="3 Point Bend",
        uids={"my_id": my_id},
        tags=["3_pt_bend", "mechanical", "flex"] + list(extra_tags),
        properties=[
            Property(
                name="flexural stress",
                value=NormalReal(stress, std=(0.01 * stress), units="MPa"),
                origin=Origin.MEASURED
            ),
            Property(
                name="flexural strain",
                value=NormalReal(strain, std=(0.01 * strain), units=""),
                origin=Origin.MEASURED
            ),
            Property(
                name="flexural modulus",
                value=NormalReal(modulus, std=(0.01 * modulus), units="MPa"),
                origin=Origin.MEASURED
            ),
            Property(
                name="deflection",
                value=NominalReal(deflection, units="mm"),
                origin=Origin.MEASURED
            )
        ]
    )
    return measurement

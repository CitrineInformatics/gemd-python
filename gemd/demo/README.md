# Example Ingesters and Object Builders

This package includes examples of working with the library.
These examples were developed in conjuction with the library, and so some may not reflect our current
understanding of best practice.
Nothing represented here is packaged to function directly as part of an ETL workflow;
rather these are intended for educational and testing purposes.


List of examples:
 - `cake`
 - `material_run_example`
 - `measurement_example`
 - `strehlow_and_cook`

---
 
### Example: `cake`

This example demonstates building a graph representation of a material manufacture process,
in this case a cake.
It includes many examples of the ways materials can be consumed by process to generate new materials.
It also includes examples of using each type of entity in the data model.
It also presents the different layers of the data model -- Templates, Specs, and Runs -- and is
configured to generate subtly different executions of the same, shared recipe.
It is based upon a yellow cake recipe, with an in-object reference to the source.

---

### Example: `material_run_example`

This example demonstrates how multiple experiments on the same sample can be represented as a
`MaterialRun` that links to multiple `MeasurementRun` objects.
Each experiment can contain measured properties, measured conditions, and specified parameters.
The ingester can optionally provide a `MaterialSpec` and/or `ProcessRun`, which are linked to the `MaterialRun` before
it is returned.
In this example, it is not possible to specify the `MeasurementSpec` since the experiments in the
input could come from different `MeasurementSpec` objects.
Rather, the data platform would create stubs, which would later be filled in or connected to
an existing `MeasurementSpec`.
Similarly, this example does not include `MaterialTemplate` or `MeasurementTemplate`, which could be
assigned to the return objects later.

---

### Example: `measurement_example`

This example demonstrates how one `MeasurementRun` can be used to store multiple properties together.
In this example of a three-point bend, the flexural stress, flexural strain, flexural modulus and deflection
are stored.
As these measurements would all share the same standard operating procedure, a user might choose to have
them all share the same `MeasurementSpec`.  As each test would be performed (presumably) on a different
artifact, they would each be assigned a different `material`.


---

### Example: `strehlow_and_cook`

This example converts the band gaps and associated metadata reported in:

> Compilation of Energy Band Gaps in Elemental and Binary Compound Semiconductors and Insulators
> W. H. Strehlow, and E. L. Cook,
> Journal of Physical and Chemical Reference Data 2, 163 (1973); doi:10.1063/1.3253115

from the [Citrine PIF](https://citrineinformatics.github.io/pif-documentation/) format into an equivalent
GEMD format.
The original source does not include a detailed material history for the samples (as this is a secondary
research effort), and so the objects are represented simply as materials procured as tested.

# Example Ingesters

This package includes example ingesters.
Currently, they focus on the "transform" and "load" steps of the ETL workflow:
given structured data (native python objects), they transform the data into the next gen object model
and write the file to disk in the next gen serialization format.
They do not deal with the extraction of structured data from native formats, nor are they packaged as
a deployable ingester.


List of examples:
 - `material_run_example`

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

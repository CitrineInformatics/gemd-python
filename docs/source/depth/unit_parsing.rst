==========================
Unit Parsing
==========================

Unit parsing is performed using the Pint_ package.
By default, Pint supports a larger set of units than the Citrine Platform.
Therefore, we include a custom unit definition file in gemd-python: `citrine_en.txt`_.
This file contains the most commonly used units and will grow over time.

In support of common patterns in materials science, we permit including scaling factors in a unit of measure.
For example, industrial researchers may have recorded historical data as ``g / 2.5 cm``.
While this could be converted a simple SI expression, that would prevent researchers from representing the data
as originally reported, thus creating a potential source of error during the input process.

Requests for support of additional units can be made by opening an issue in the `gemd-python repository`_ on github.

.. _Pint: https://pint.readthedocs.io/en/stable/
.. _citrine_en.txt: https://github.com/CitrineInformatics/gemd-python/blob/main/gemd/units/citrine_en.txt
.. _GEMD-python repository: https://github.com/CitrineInformatics/gemd-python

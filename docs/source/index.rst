.. GEMD documentation master file, created by
   sphinx-quickstart on Thu Aug 22 14:40:14 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the GEMD-Python Documentation!
===================================================

This site documents the Python implementation of the Graphical Expression of Materials Data (GEMD) model.
GEMD is an open source data format developed by `Citrine Informatics <https://citrine.io/>`_ for representing
data in materials in a `FAIR <https://www.go-fair.org/fair-principles/>`_ and transformable manner.
Documentation of the underlying data model can be found `here <https://citrineinformatics.github.io/gemd-docs/>`_.

To learn about the details of specific classes, please see the module index.

Installation
------------

The latest release can be installed via `pip`:

.. code:: bash

  pip install gemd

or a specific version can be installed, for example:

.. code:: bash

  pip install gemd==2.1.1

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :numbered: 4

   depth/unit_parsing
   depth/serialization
   API Reference <reference/modules>

Indices
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

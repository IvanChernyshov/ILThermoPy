======================================
Welcome to ILThermoPy's documentation!
======================================

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   Cookbook <source/cookbook.ipynb>
   Package API <source/api>
   Changelog <source/changelog>


**ILThermoPy** is an unofficial Python package for retrieving data from
`ILThermo 2.0`_ and enriching ionic-liquid records with molecular identifiers
such as SMILES. It is intended for cheminformatics, molecular thermodynamics,
and machine-learning workflows that need ILThermo data in a more
structure-aware form.

Status and scope
================

* Usable package for accessing ILThermo 2.0 data and combining retrieved records
  with stored molecular-structure annotations.
* Unofficial interface: ILThermoPy is not affiliated with, maintained by, or
  endorsed by NIST.
* External-service-dependent: ILThermo 2.0 does not provide a stable public web
  API, so this package depends on the current behavior of the ILThermo web
  service.
* Molecular-identifier enrichment depends on stored mappings from ILThermo
  compound identifiers to manually checked structural data; new ILThermo
  updates may require refreshing those mappings.
* Intended for cheminformatics, molecular thermodynamics, and ML-ready
  ionic-liquid data workflows.

What problem does it solve?
===========================

ILThermo 2.0 contains experimental physicochemical-property data for ionic
liquids, but the public web interface primarily describes molecular components
by names. For many downstream workflows, names are not enough: cheminformatics,
substructure search, descriptor generation, data cleaning, and ML model building
usually require machine-readable molecular identifiers.

ILThermoPy bridges this gap by retrieving ILThermo records and adding stored
SMILES annotations for known ionic-liquid components. The structural annotations
were prepared through semi-automatic name-to-structure conversion followed by
manual validation, making the extracted data easier to use in computational
chemistry and data-driven thermodynamics workflows.

Typical use cases include:

* collecting ILThermo records for selected properties, compounds, or years;
* preparing ionic-liquid datasets for descriptor calculation and ML pipelines;
* linking thermodynamic measurements to cation/anion structures;
* checking which ILThermo compounds already have stored structural annotations;
* updating local structural mappings when the external ILThermo database
  changes.

The package is intentionally small. It should be treated as a practical access
and enrichment layer over an external web service, not as an official ILThermo
API or a complete curated thermodynamic database.

Installation
============

ILThermoPy can be installed from the `PyPI package`_:

.. code-block:: bash

   pip install ilthermopy


Requirements
============

1. Python 3.7+;
2. requests;
3. pandas;
4. importlib_resources for Python 3.7 and 3.8.


Useful links
============

1. `ILThermo 2.0`_: public web application for the ILThermo 2.0 database.
2. `Documentation`_: cookbook, API reference, and changelog.
3. `PyPI package`_: package distribution page.
4. `GitHub repository`_: source code and release history.
5. `Issue tracker`_: bug reports and maintenance notes.
6. `Update tools`_: scripts for semi-automatic refresh of structural
   information after ILThermo database updates.


Citation
========

If ILThermoPy is useful in your work, please cite the Zenodo concept DOI
(all versions), which resolves to the latest archived release:

   Ivan Yu. Chernyshov. (2026). *ILThermoPy: unofficial ILThermo 2.0
   access and SMILES enrichment for ionic-liquid data workflows* [Computer
   software]. Zenodo. https://doi.org/10.5281/zenodo.20218373

Citation metadata is also provided in the repository ``CITATION.cff`` file.


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. _ILThermo 2.0: https://ilthermo.boulder.nist.gov/
.. _Documentation: https://mucommons.github.io/ILThermoPy/
.. _PyPI package: https://pypi.org/project/ilthermopy/
.. _GitHub repository: https://github.com/muCommons/ILThermoPy
.. _Issue tracker: https://github.com/muCommons/ILThermoPy/issues
.. _Update tools: https://github.com/muCommons/ILThermoPy/tree/main/update

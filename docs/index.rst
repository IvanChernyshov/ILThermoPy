======================================
Welcome to ILThermoPy's documentation!
======================================

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:
   
   Cookbook <source/cookbook>
   Package API <source/api>
   Changelog <source/changelog>


**ILThermoPy** is a Python library to access `ILThermo 2.0`_, which is the NIST standard reference database, containing measured physico-chemical properties for a wide spectrum of ionic liquids.
Despite the significant amount of stored data, ILThermo 2.0 cannot be used for machine learning, parametrization of empirical physical models, and other data-driven approaches as is.
The reason is that ILThermo 2.0 describes molecular structure of IL's components with a chemical name only, whereas SMILES, InChI and other structure identifiers are not available.

**ILThermoPy** solves this problem via the preliminary semi-automatic conversion of compound names to SMILES with subsequent manual validation.
This allows one to conduct a substructural search and to immediately generate chemoinformatic descriptors for the extracted data.

.. note::
   There is no official web API available to access ILThermo 2.0, therefore the stability of this library depends on the stability of the JSON/javascript framework of the webservice.

.. warning::
   ILThermo 2.0 database is regularly updated, at least once a year.
   Those updates change internal compound IDs, which are used to add SMILES to the extracted data.
   Therefore, after database's update old versions of **ILThermoPy** can fail to retrieve structural data at least for some of the new entries.


Installation
============

**ILThermoPy** can be installed as a `PyPI package`_:

.. code-block::
   
   > pip install ilthermopy


Requirements
============

1. Python 3.7+;

2. requests;

3. pandas;

4. importlib_resources (for Python 3.7 and 3.8).


Useful links
============

1. `ILThermo 2.0`_: webapp accessing ILThermo 2.0 database.
2. `GitHub`_: GitHub page of the package.
3. `PyPI package`_: PyPI page of the package.


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`



.. _ILThermo 2.0: https://ilthermo.boulder.nist.gov/
.. _GitHub: https://github.com/IvanChernyshov/ILThermoPy
.. _PyPI package: https://pypi.org/project/ilthermopy/

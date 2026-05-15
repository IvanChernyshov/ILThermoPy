Changelog
=========

1.1.2
-----

* Refreshes public-facing documentation and package metadata after the move to
  the ``muCommons`` GitHub organization.

* Updates repository, documentation, issue-tracker, and changelog links to the
  new public locations.

* Clarifies project status: ILThermoPy is an unofficial ILThermo 2.0
  access/enrichment package, is external-service-dependent, and is not
  affiliated with or endorsed by NIST.

* Updates PyPI-facing metadata, including the short description, keywords,
  project URLs, and development-status classifier.

* Adds citation metadata via ``CITATION.cff`` to prepare the repository for
  Zenodo release archiving.

* No runtime-code changes, public API changes, or dependency changes.


1.1.1
-----

* Adds small code fixes.

* Migrates package info from ``setup.cfg`` to ``pyproject.toml``.

* Changes layout to ``src``.

* Adds tests.


1.1.0
-----

* Updates stored structural data (up to June 4, 2024).

* Renames the ``GetCompounds`` function to :py:func:`ilthermopy.compound_list.GetSavedCompounds`.

* Adds functionality for semi-automatic update of structural information of ILThermo compounds.


1.0.0
-----

First release.



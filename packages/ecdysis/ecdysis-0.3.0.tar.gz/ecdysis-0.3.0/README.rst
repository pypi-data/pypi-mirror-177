=======
ecdysis
=======


.. image:: https://img.shields.io/pypi/v/ecdysis.svg
        :target: https://pypi.python.org/pypi/ecdysis

.. image:: https://img.shields.io/travis/datagazing/ecdysis.svg
        :target: https://travis-ci.com/datagazing/ecdysis

.. image:: https://readthedocs.org/projects/ecdysis/badge/?version=latest
        :target: https://ecdysis.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Interface to pyprocessmacro

Features
--------

* Command-line interface
* Handle loading data from common formats (csv, tsv, xlsx, sav, ...)
* Convenience function for examining data
* Save output in familiar PROCESS text format
* Supports most or all pyprocessmacro options

Examples
--------

.. code-block:: console

  $ ecdysis -h
  ...
  $ ecdysis -i data.csv --summarize
  ...
  $ ecdysis -i data.csv -X xvar -M mvar -Y yvar -o results.txt
  ...

Limitations
-----------

* Relies on pandect which relies on pyreadstat, which has issues with
  reading dta (Stata) format files
* Expects variables to be numeric

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

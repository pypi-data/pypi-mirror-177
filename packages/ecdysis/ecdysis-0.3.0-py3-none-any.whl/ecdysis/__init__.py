"""
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

"""

__author__ = """Brendan Strejcek"""
__email__ = 'brendan@datagazing.com'
__version__ = '0.3.0'

from .ecdysis import main # noqa F401

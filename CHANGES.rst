ChangeLog
=========


`2.1.1 (unreleased) <https://github.com/scaleway/port-range/compare/v2.1.0...develop>`_
---------------------------------------------------------------------------------------

 * No changes yet.


`2.1.0 (2017-08-02) <https://github.com/scaleway/port-range/compare/v2.0.0...v2.1.0>`_
--------------------------------------------------------------------------------------

* Rename ``port_lenght`` property to ``port_length``.


`2.0.0 (2015-12-19) <https://github.com/scaleway/port-range/compare/v1.0.5...v2.0.0>`_
--------------------------------------------------------------------------------------

* Refactor parsing. Makes normal mode stricter and ``strict`` mode more
  rigorous.
* Expose ``is_single_port`` and ``is_cidr`` properties in ``repr()``.
* Unittests covers 100% of code.
* Add default ``isort`` config.
* Run unittests against Python 3.3, 3.5, 3.6-dev, 3.7-dev, PyPy2.7 and PyPy3.3.
* Remove popularity badge: PyPI download counters are broken and no longer
  displayed.
* Move ``coverage`` config to ``setup.cfg``.
* Add ``test`` and ``develop`` dependencies.
* Only show latest changes in the long description of the package instead of
  the full changelog.
* Replace ``pep8`` package by ``pycodestyle``.
* Enforce ``pycodestyle`` checks in Travis CI jobs.
* Test production of packages in Travis CI jobs.
* Always check for package metadata in Travis CI jobs.
* Make wheels generated under Python 2 environment available for Python 3 too.
* Add link to full changelog in package's long description.


`1.0.5 (2015-11-23) <https://github.com/scaleway/port-range/compare/v1.0.4...v1.0.5>`_
--------------------------------------------------------------------------------------

* Add ``bumpversion`` config.


`1.0.4 (2015-11-23) <https://github.com/scaleway/port-range/compare/v1.0.3...v1.0.4>`_
--------------------------------------------------------------------------------------

* Switch from ``coveralls.io`` to ``codecov.io``.


`1.0.3 (2015-04-10) <https://github.com/scaleway/port-range/compare/v1.0.2...v1.0.3>`_
--------------------------------------------------------------------------------------

* Raise exception when trying to render non-CIDR-like port ranges with a CIDR
  notation.


`1.0.2 (2015-04-07) <https://github.com/scaleway/port-range/compare/v1.0.1...v1.0.2>`_
--------------------------------------------------------------------------------------

* Update all Online Labs references to Scaleway.


`1.0.1 (2015-03-26) <https://github.com/scaleway/port-range/compare/v1.0.0...v1.0.1>`_
--------------------------------------------------------------------------------------

* Check code coverage thanks to ``coveralls.io``.


`1.0.0 (2014-12-11) <https://github.com/scaleway/port-range/compare/v0.1.0...v1.0.0>`_
--------------------------------------------------------------------------------------

* Split out port range helpers into its own stand-alone package.
* First public release.


`0.1.0 (2014-02-17) <https://github.com/scaleway/port-range/compare/ffc707...v0.1.0>`_
--------------------------------------------------------------------------------------

* First internal release.


`0.0.0 (2014-02-11) <https://github.com/scaleway/port-range/commit/ffc707>`_
----------------------------------------------------------------------------

* First commit.

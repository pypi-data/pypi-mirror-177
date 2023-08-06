=================================================
pvenv: Easy python virtual environment management
=================================================

.. image:: https://github.com/spapanik/pvenv/actions/workflows/build.yml/badge.svg
  :alt: Build
  :target: https://github.com/spapanik/pvenv/actions/workflows/build.yml
.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/pvenv.svg
  :alt: Total alerts
  :target: https://lgtm.com/projects/g/spapanik/pvenv/alerts/
.. image:: https://img.shields.io/github/license/spapanik/pvenv
  :alt: License
  :target: https://github.com/spapanik/pvenv/blob/main/LICENSE.txt
.. image:: https://img.shields.io/pypi/v/pvenv
  :alt: PyPI
  :target: https://pypi.org/project/pvenv
.. image:: https://pepy.tech/badge/pvenv
  :alt: Downloads
  :target: https://pepy.tech/project/pvenv
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style
  :target: https://github.com/psf/black


In a nutshell
-------------

Installation
^^^^^^^^^^^^

The easiest way is to use pipx to install ``pvenv``.

.. code:: console

   $ pipx install pvenv

Please make sure that the correct directory is added to your path. This
depends on the OS.

Usage
^^^^^

Run ``pvenv`` to get the path to be sourced in the shell rc:

.. code:: console

   $ pipx install pvenv

After that, you can use the following commands:

* invenv
* outvenv
* avenv
* dvenv
* lsvenv
* mkvenv
* rmvenv

or as subcommands of venv:

* venv in
* venv out
* venv activate
* venv deactivate
* venv list
* venv make
* venv rm

Links
-----

- `Documentation`_
- `Changelog`_


.. _Changelog: https://github.com/spapanik/pvenv/blob/main/CHANGELOG.rst
.. _Documentation: https://p-venv.readthedocs.io/en/stable/

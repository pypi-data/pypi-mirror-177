# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pvenv', 'pvenv.subcommands']

package_data = \
{'': ['*'], 'pvenv': ['scripts/*']}

entry_points = \
{'console_scripts': ['pvenv = pvenv.main:main']}

setup_kwargs = {
    'name': 'pvenv',
    'version': '0.4.0',
    'description': 'Easy python virtual environment management',
    'long_description': '=================================================\npvenv: Easy python virtual environment management\n=================================================\n\n.. image:: https://github.com/spapanik/pvenv/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/pvenv/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/pvenv.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/pvenv/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/pvenv\n  :alt: License\n  :target: https://github.com/spapanik/pvenv/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/pvenv\n  :alt: PyPI\n  :target: https://pypi.org/project/pvenv\n.. image:: https://pepy.tech/badge/pvenv\n  :alt: Downloads\n  :target: https://pepy.tech/project/pvenv\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use pipx to install ``pvenv``.\n\n.. code:: console\n\n   $ pipx install pvenv\n\nPlease make sure that the correct directory is added to your path. This\ndepends on the OS.\n\nRun ``pvenv`` to get the path to be sourced in the shell rc:\n\n.. code:: console\n\n   $ pvenv\n\nUsage\n^^^^^\n\nYou can use the following commands:\n\n* `venv activate` (aliased to `avenv`) to activate a virtual environment\n* `venv deactivate` (aliased to `dvenv`) to deactivate a virtual environment\n* `venv list` (aliased to `lsvenv`) to list all the virtual environments\n* `venv make` (aliased to `mkvenv`) to create a new virtual environment\n* `venv rm` (aliased to `rmvenv`) to remove a virtual environment\n\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _Changelog: https://github.com/spapanik/pvenv/blob/main/CHANGELOG.rst\n.. _Documentation: https://p-venv.readthedocs.io/en/stable/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spapanik/pvenv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

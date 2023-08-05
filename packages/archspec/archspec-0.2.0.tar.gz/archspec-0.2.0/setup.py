# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archspec', 'archspec.cpu']

package_data = \
{'': ['*'],
 'archspec': ['json/*',
              'json/.github/workflows/*',
              'json/.pytest_cache/*',
              'json/.pytest_cache/v/cache/*',
              'json/cpu/*',
              'json/tests/targets/*']}

install_requires = \
['click>=8,<9']

entry_points = \
{'console_scripts': ['archspec = archspec.cli:main']}

setup_kwargs = {
    'name': 'archspec',
    'version': '0.2.0',
    'description': 'A library to query system architecture',
    'long_description': "# Archspec (Python bindings)\n\n[![CI](https://github.com/archspec/archspec/workflows/Unit%20tests/badge.svg)](https://github.com/archspec/archspec/actions)\n[![CodeCov](https://codecov.io/gh/archspec/archspec/branch/master/graph/badge.svg)](https://codecov.io/gh/archspec/archspec)\n[![Documentation Status](https://readthedocs.org/projects/archspec/badge/?version=latest)](https://archspec.readthedocs.io/en/latest/?badge=latest)\n\nArchspec aims at providing a standard set of human-understandable labels for\nvarious aspects of a system architecture  like CPU, network fabrics, etc. and\nAPIs to detect, query and compare them.\n\nThis project grew out of [Spack](https://spack.io/) and is currently under\nactive development. At present it supports APIs to detect and model\ncompatibility relationships among different CPU microarchitectures.\n\n## Getting started with development\n\nThe `archspec` Python package needs [poetry](https://python-poetry.org/) to\nbe installed from VCS sources. The preferred method to install it is via\nits custom installer outside of any virtual environment:\n\n```console\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\nYou can refer to [Poetry's documentation](https://python-poetry.org/docs/#installation)\nfor further details or for other methods to install this tool. You'll also need `tox`\nto run unit test:\n\n```console\npip install --user tox\n```\n\nFinally, you'll need to clone the repository:\n\n```console\ngit clone --recursive https://github.com/archspec/archspec.git\n```\n\n### Running unit tests\n\nOnce you have your environment ready you can run `archspec` unit tests\nusing ``tox`` from the root of the repository:\n\n```console\n$ tox\n  [ ... ]\n  py27: commands succeeded\n  py35: commands succeeded\n  py36: commands succeeded\n  py37: commands succeeded\n  py38: commands succeeded\n  pylint: commands succeeded\n  flake8: commands succeeded\n  black: commands succeeded\n  congratulations :)\n```\n\n## Citing Archspec\n\nIf you are referencing `archspec` in a publication, please cite the following\npaper:\n\n* Massimiliano Culpo, Gregory Becker, Carlos Eduardo Arango Gutierrez, Kenneth\n   Hoste, and Todd Gamblin.\n   [**`archspec`: A library for detecting, labeling, and reasoning about\n   microarchitectures**](https://tgamblin.github.io/pubs/archspec-canopie-hpc-2020.pdf).\n   In *2nd International Workshop on Containers and New Orchestration Paradigms\n   for Isolated Environments in HPC (CANOPIE-HPC'20)*, Online Event, November\n   12, 2020.\n\n## License\n\nArchspec is distributed under the terms of both the MIT license and the\nApache License (Version 2.0). Users may choose either license, at their\noption.\n\nAll new contributions must be made under both the MIT and Apache-2.0\nlicenses.\n\nSee [LICENSE-MIT](https://github.com/archspec/archspec/blob/master/LICENSE-MIT),\n[LICENSE-APACHE](https://github.com/archspec/archspec/blob/master/LICENSE-APACHE),\n[COPYRIGHT](https://github.com/archspec/archspec/blob/master/COPYRIGHT), and\n[NOTICE](https://github.com/archspec/archspec/blob/master/NOTICE) for details.\n\nSPDX-License-Identifier: (Apache-2.0 OR MIT)\n\nLLNL-CODE-811653\n",
    'author': 'archspec developers',
    'author_email': 'maintainers@spack.io',
    'maintainer': 'Greg Becker',
    'maintainer_email': 'maintainers@spack.io',
    'url': 'https://github.com/archspec/archspec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)

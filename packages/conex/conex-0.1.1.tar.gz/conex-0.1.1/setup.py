# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['conanapi',
 'conanapi.commands',
 'conanapi.internal',
 'conanapi.types',
 'conex',
 'conex.cli_parsers',
 'conex.commands',
 'conex.exceptions',
 'conex.internal',
 'conex.internal.fakes']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11.4,<0.12.0']

entry_points = \
{'console_scripts': ['conex = conex.cli:main']}

setup_kwargs = {
    'name': 'conex',
    'version': '0.1.1',
    'description': 'Utilities for simplifying conan usage',
    'long_description': None,
    'author': 'Nicholas Johnson',
    'author_email': 'nicholas.m.j@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['tofspec', 'tofspec.cli', 'tofspec.cli.commands', 'tofspec.db']

package_data = \
{'': ['*'], 'tofspec': ['config/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.4,<9.0.0',
 'dask>=2022.4.1,<2023.0.0',
 'h5py>=3.6.0,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'rich-click>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['tofspec = tofspec.cli:main']}

setup_kwargs = {
    'name': 'py-tofspec',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Joe Palmo',
    'author_email': 'jpalmo21@amherst.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

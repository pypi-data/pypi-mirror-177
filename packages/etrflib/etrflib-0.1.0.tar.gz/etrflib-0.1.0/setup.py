# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etrflib']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'cffi>=1.15.0,<2.0.0',
 'ipython>=8.3.0,<9.0.0',
 'miniopy-async>=1.11,<2.0',
 'pydantic>=1.10.2,<2.0.0',
 'pydffi>=0.9.3,<0.10.0',
 'pyfiglet>=0.8.post1,<0.9',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['etrflib = etrflib.main:app']}

setup_kwargs = {
    'name': 'etrflib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Francesco Bartoli',
    'author_email': 'francesco.bartoli@geobeyond.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weatherforecastcli']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'tzdata>=2022.6,<2023.0']

entry_points = \
{'console_scripts': ['weather = weatherforecastcli.main:main']}

setup_kwargs = {
    'name': 'weatherforecastcli',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

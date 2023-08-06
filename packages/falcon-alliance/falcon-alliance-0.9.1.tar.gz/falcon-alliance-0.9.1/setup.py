# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['falcon_alliance',
 'falcon_alliance.plotting',
 'falcon_alliance.schemas',
 'falcon_alliance.tests',
 'falcon_alliance.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<3.9.0',
 'matplotlib>=3.6.0,<3.7.0',
 'python-dotenv>=0.19,<1.0',
 'scipy>=1.9.2,<1.10.0']

setup_kwargs = {
    'name': 'falcon-alliance',
    'version': '0.9.1',
    'description': 'A Pythonic library that attains FRC-related information from sources like The Blue Alliance and more.',
    'long_description': None,
    'author': 'The Falcons - Team 4099',
    'author_email': 'contact@team4099.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/team4099/FalconAlliance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['greet_app']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['greet-app = greet_app.main:app']}

setup_kwargs = {
    'name': 'greet-app',
    'version': '0.2.0',
    'description': '',
    'long_description': 'My-app',
    'author': 'Kamil Woźniak',
    'author_email': 'jestem.kamil.wozniak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

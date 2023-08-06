# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soft_test']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'kivy>=2.1.0,<3.0.0', 'kivymd>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['app-cli = app.cli:cli']}

setup_kwargs = {
    'name': 'soft-test',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'elbulidur',
    'author_email': 'juliocezar.marketing@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

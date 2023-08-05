# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apix']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'apix',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Arwichok',
    'author_email': 'me@arwi.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdoc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hdoc',
    'version': '0.1.0',
    'description': '',
    'long_description': '# hdoc\n\nThis project holds Python bindings for [hdoc](https://hdoc.io).\n',
    'author': 'hdoc',
    'author_email': 'pypi@hdoc.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

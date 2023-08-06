# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dhydrogen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dhydrogen',
    'version': '0.0.0',
    'description': 'The lighter way to save.',
    'long_description': '# dhydrogen\n\nThe lighter way to save.\n\nnote: do this later',
    'author': 'Jase',
    'author_email': 'jasew@getdeuterium.win',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

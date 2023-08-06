# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['accessory']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'accessory',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Accessory\n\nGeneralized functional getters and setters, via profunctor optics.\n',
    'author': 'Simon Zeng',
    'author_email': 'contact@simonzeng.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

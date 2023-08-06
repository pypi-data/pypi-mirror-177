# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyjax']

package_data = \
{'': ['*']}

install_requires = \
['jax==0.3.15']

setup_kwargs = {
    'name': 'easyjax',
    'version': '0.1.1',
    'description': 'Facilitates machine learning development for JAX.',
    'long_description': '# EasyJax \n\n> work-in-progress. \n\nEasyJax is a python package that facilitates machine learning development for JAX. It does that by providing:\n\n1. A high-level API for machine learning workflows in JAX (specifically a trainer, experiment parent class). \n2. Several machine learning specific utilities for working with JAX (e.g., `ml.update_step`). \n\n',
    'author': 'Rohan Sikand',
    'author_email': 'rsikand29@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rosikand/easyjax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

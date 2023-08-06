# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tapmusic-cli']
install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'tapmusic-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'atomheartbrother',
    'author_email': 'rhnsolomon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

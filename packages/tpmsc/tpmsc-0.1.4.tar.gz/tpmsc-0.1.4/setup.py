# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tpmsc']
install_requires = \
['click>=8.1.3,<9.0.0', 'pathlib>=1.0.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['tpmsc = tpmsc:main']}

setup_kwargs = {
    'name': 'tpmsc',
    'version': '0.1.4',
    'description': 'CLI tool to download music collages from tapmusic.net',
    'long_description': 'None',
    'author': 'atomheartbrother',
    'author_email': 'rhnsolomon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

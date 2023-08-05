# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myprj']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['myprj = myprj.cli:cli']}

setup_kwargs = {
    'name': 'python-project-poetry-template',
    'version': '0.11.0b1',
    'description': 'Python Project Poetry Template',
    'long_description': 'None',
    'author': 'mrjk',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

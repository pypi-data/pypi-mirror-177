# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_tictactoe']

package_data = \
{'': ['*']}

modules = \
['tictactoe']
entry_points = \
{'console_scripts': ['djtictactoe = dj_tictactoe.Main:cli']}

setup_kwargs = {
    'name': 'dj-tictactoe',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'dongjin2008',
    'author_email': 'dkim@icsparis.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

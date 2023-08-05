# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycistem', 'pycistem.core', 'pycistem.database', 'pycistem.programs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'appdirs>=1.4.4,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'rich>=11.0.0,<12.0.0',
 'starfile>=0.4.11,<0.5.0']

setup_kwargs = {
    'name': 'pycistem',
    'version': '0.1.5',
    'description': '',
    'long_description': 'None',
    'author': 'Johannes Elferich',
    'author_email': 'jojotux123@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

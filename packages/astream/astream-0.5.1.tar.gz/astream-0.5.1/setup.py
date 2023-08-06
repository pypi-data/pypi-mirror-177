# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astream', 'astream.experimental']

package_data = \
{'': ['*']}

install_requires = \
['PyHeat>=0.2,<0.3',
 'asyncio>=3.4.3,<4.0.0',
 'decorator>=5.1.1,<6.0.0',
 'lazy-object-proxy>=1.8.0,<2.0.0',
 'mypy>=0.991,<0.992',
 'wrapt>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'astream',
    'version': '0.5.1',
    'description': '',
    'long_description': None,
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapsl']

package_data = \
{'': ['*']}

install_requires = \
['alog>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'yapsl',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Benjamin Bruno Meier',
    'author_email': 'benjamin.meier70@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

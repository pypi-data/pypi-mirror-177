# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protokol', 'protokol.transports']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'nats-py>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'protokol',
    'version': '1.4.1',
    'description': 'NATS-oriented RPC and Event protocol',
    'long_description': None,
    'author': 'Sergey Zhegunya',
    'author_email': 'harmonicsseven@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

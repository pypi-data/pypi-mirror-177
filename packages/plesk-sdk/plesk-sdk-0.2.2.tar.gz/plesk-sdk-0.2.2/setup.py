# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plesk_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'plesk-sdk',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'khasanovmma',
    'author_email': 'khasanovmma010@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

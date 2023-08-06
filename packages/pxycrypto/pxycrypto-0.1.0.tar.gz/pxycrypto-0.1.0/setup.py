# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pxycrypto']

package_data = \
{'': ['*'], 'pxycrypto': ['assets/*']}

setup_kwargs = {
    'name': 'pxycrypto',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Z1R343L',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

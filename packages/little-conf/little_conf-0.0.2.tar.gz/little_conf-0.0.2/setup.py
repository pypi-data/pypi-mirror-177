# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['little_conf']

package_data = \
{'': ['*']}

install_requires = \
['deepmerge>=1.1.0,<2.0.0',
 'pydantic>=1.8.0,<2.0.0',
 'pytest>=6.2.4,<7.0.0',
 'pyyaml>5.0.0']

setup_kwargs = {
    'name': 'little-conf',
    'version': '0.0.2',
    'description': 'Simple library for service configuration',
    'long_description': 'None',
    'author': 'smartleks',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

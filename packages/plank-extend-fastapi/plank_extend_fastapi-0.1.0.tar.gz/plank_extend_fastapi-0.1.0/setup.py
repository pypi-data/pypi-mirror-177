# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plank',
 'plank.decorator',
 'plank.descriptor',
 'plank.server.fastapi',
 'plank.support',
 'plank.support.fastapi']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.78.0,<0.79.0',
 'plank>=0.1.0,<0.2.0',
 'pydantic>=1.9.2,<2.0.0',
 'uvicorn>=0.17.6,<0.18.0']

setup_kwargs = {
    'name': 'plank-extend-fastapi',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Grady Zhuo',
    'author_email': 'grady@ospark.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

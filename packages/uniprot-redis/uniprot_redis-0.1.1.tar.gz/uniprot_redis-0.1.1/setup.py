# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uniprot_redis', 'uniprot_redis.store']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'fastapi>=0.79.0,<0.80.0',
 'pyproteinsext>=3.0.3,<4.0.0',
 'pyrediscore>=0.3.0,<0.4.0',
 'uvicorn>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'uniprot-redis',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Cecile Hilpert',
    'author_email': 'cecile.hilpert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['name_that_hash']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2', 'rich>=11.0.0']

entry_points = \
{'console_scripts': ['name-that-hash = name_that_hash.runner:main',
                     'nth = name_that_hash.runner:main']}

setup_kwargs = {
    'name': 'name-that-hash',
    'version': '1.11.0',
    'description': 'The Modern Hash Identification System',
    'long_description': 'None',
    'author': 'autumn',
    'author_email': 'autumn@skerritt.blog',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

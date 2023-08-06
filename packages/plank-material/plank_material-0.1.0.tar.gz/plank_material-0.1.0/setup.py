# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plank',
 'plank.configuration',
 'plank.configuration.builtins',
 'plank.context']

package_data = \
{'': ['*']}

install_requires = \
['plank-core>=0.1.0,<0.2.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'plank-material',
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

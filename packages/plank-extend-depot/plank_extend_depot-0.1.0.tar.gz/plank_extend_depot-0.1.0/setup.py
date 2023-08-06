# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plank', 'plank.depot', 'plank.depot.storage']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'ndjson>=0.3.1,<0.4.0',
 'packaging>=21.3,<22.0',
 'pandas>=1.4.2,<2.0.0',
 'plank>=0.1.0,<0.2.0',
 'tables>=3.7.0,<4.0.0']

setup_kwargs = {
    'name': 'plank-extend-depot',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zashcore']

package_data = \
{'': ['*']}

install_requires = \
['structlog>=22.2.0,<23.0.0']

setup_kwargs = {
    'name': 'zashcore',
    'version': '0.2.0',
    'description': 'Core libs for zash',
    'long_description': 'None',
    'author': 'Efe',
    'author_email': 'efe@joinzash.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

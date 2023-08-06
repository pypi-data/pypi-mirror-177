# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_tools_info']

package_data = \
{'': ['*']}

install_requires = \
['tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'cli-tools-info',
    'version': '1.0.5',
    'description': '',
    'long_description': None,
    'author': 'Erik Lilja',
    'author_email': 'erik@rkllj.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

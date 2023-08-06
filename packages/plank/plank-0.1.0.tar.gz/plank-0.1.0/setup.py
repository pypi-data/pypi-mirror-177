# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plank',
 'plank.app',
 'plank.decorator',
 'plank.descriptor',
 'plank.plugin',
 'plank.plugin.asset',
 'plank.server',
 'plank.server.action',
 'plank.server.connector',
 'plank.server.message',
 'plank.serving',
 'plank.utils',
 'plank.utils.command']

package_data = \
{'': ['*'], 'plank': ['resource/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'envparse>=0.2.0,<0.3.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'plank-core>=0.1.0,<0.2.0',
 'plank-material>=0.1.0,<0.2.0',
 'plank-tool-logger>=0.1.0,<0.2.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['plank = plank.utils.command:root_cmd']}

setup_kwargs = {
    'name': 'plank',
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
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

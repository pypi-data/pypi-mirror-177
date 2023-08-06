# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kchd', 'kchd.controllers', 'kchd.driver']

package_data = \
{'': ['*']}

install_requires = \
['astoria>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['kchd = kchd:main']}

setup_kwargs = {
    'name': 'kchd',
    'version': '0.4.1',
    'description': 'KCH LED Daemon',
    'long_description': 'None',
    'author': 'Dan Trickey',
    'author_email': 'dtrickey@studentrobotics.org',
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

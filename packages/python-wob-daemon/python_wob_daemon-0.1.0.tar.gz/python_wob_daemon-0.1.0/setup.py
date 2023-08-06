# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_wob_daemon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-wob-daemon',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Manuel Brea',
    'author_email': 'm.brea.carreras@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

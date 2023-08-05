# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphframes_wrapper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'graphframes-wrapper',
    'version': '0.5.0.0',
    'description': '',
    'long_description': 'a graphframes wrapper package',
    'author': 'Anthony Edwards',
    'author_email': 'anthonygedwards93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

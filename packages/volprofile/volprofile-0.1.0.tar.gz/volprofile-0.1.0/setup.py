# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volprofile']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'volprofile',
    'version': '0.1.0',
    'description': 'calculate the volume profile in a flexible manner!',
    'long_description': '',
    'author': 'maghrebi',
    'author_email': 'sajad.faghfoor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kip_inca']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kip-inca',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Thomas Danckaert',
    'author_email': 'thomas.danckaert@vito.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

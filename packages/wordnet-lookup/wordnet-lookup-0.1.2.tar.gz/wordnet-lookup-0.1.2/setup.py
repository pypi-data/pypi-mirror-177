# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordnet_lookup', 'wordnet_lookup.os']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'wordnet-lookup',
    'version': '0.1.2',
    'description': 'Static Dictionaries for Rapid Wordnet Lookups',
    'long_description': '',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/wordnet-lookup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)

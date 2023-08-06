# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_parse_time',
 'fast_parse_time.bp',
 'fast_parse_time.dmo',
 'fast_parse_time.dto',
 'fast_parse_time.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'word2number']

setup_kwargs = {
    'name': 'fast-parse-time',
    'version': '0.1.6',
    'description': 'Natural Language (NLP) Extraction of Date and Time',
    'long_description': '',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/fast-parse-time',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)

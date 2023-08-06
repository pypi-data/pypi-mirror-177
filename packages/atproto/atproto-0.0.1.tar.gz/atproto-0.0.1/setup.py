# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atproto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'atproto',
    'version': '0.0.1',
    'description': 'atproto SDK',
    'long_description': '## Work in progress\n',
    'author': 'Ilya (Marshal)',
    'author_email': 'ilya@marshal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MarshalX/atproto',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

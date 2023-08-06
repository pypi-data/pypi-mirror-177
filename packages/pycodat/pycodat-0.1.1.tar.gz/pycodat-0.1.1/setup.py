# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycodat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycodat',
    'version': '0.1.1',
    'description': '',
    'long_description': '# pyCodat\n\nA wrapper around the Codat API.\n\n',
    'author': 'max-addison',
    'author_email': '105925792+max-addison@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

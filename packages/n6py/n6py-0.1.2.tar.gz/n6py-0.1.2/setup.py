# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['n6py', 'n6py.stats']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'n6py',
    'version': '0.1.2',
    'description': 'N6 AI Python Tools',
    'long_description': '# N6 Py',
    'author': 'Sergej Samsonenko',
    'author_email': 'contact@sergej.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

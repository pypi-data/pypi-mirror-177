# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['n6py', 'n6py.encode', 'n6py.stats']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'n6py',
    'version': '0.1.3',
    'description': 'N6 AI Python Tools',
    'long_description': '# N6 Py\n\nN6 AI Python Tools.\n\n## About\n\nTooling for common problems in Scientific Computing, Machine Learning and Deep Learning.\n\n## Installing\n\n**pip**\n```sh\npip install n6py\n```\n\n**Poetry**\n```sh\npoerty add n6py\n```',
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

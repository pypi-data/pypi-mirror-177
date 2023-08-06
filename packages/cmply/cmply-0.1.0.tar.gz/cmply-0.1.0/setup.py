# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmply', 'docker_runner']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'docker>=6.0.1,<7.0.0',
 'pyyaml>=6.0,<7.0',
 'schema>=0.7.5,<0.8.0',
 'termcolor>=2.1.1,<3.0.0']

entry_points = \
{'console_scripts': ['cmply = cmply:main']}

setup_kwargs = {
    'name': 'cmply',
    'version': '0.1.0',
    'description': 'A simple tool to validate if a repository adhears to specified rules.',
    'long_description': '# cmply',
    'author': 'Paul Selibas',
    'author_email': 'pselibas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

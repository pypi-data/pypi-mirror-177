# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmply', 'docker_runner']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'docker>5',
 'pyyaml>=6.0,<7.0',
 'schema>=0.7.5,<0.8.0',
 'termcolor>=2.1.1,<3.0.0']

entry_points = \
{'console_scripts': ['cmply = cmply:main']}

setup_kwargs = {
    'name': 'cmply',
    'version': '0.1.2',
    'description': 'A simple tool to validate if a repository adhears to specified rules.',
    'long_description': '# cmply\n\n[![PyPI version](https://img.shields.io/pypi/v/cmply.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/cmply)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/cmply.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/cmply)\n[![PyPI downloads](https://img.shields.io/pypi/dm/cmply.svg)](https://pypistats.org/packages/cmply)\n[![Licence](https://img.shields.io/github/license/pselibas/cmply.svg)](LICENSE.txt)\n\n\n## Installation\n\n```bash\npython3 -m pip install --upgrade cmply\n```\n\n## Introduction\n\nCmply is a tool used to run a set of rules against a repository.\nThe output will show the result of what rules fail or pass.\nThere is provision for different levels of failures. These levels are `info, warning, fail and security`.\nThe target can be a local folder or a git repository. \nIf a git repository is specified, the local git is used with any configure authentication relative to the local system.\n\n## Usage\n```bash\nusage: cmply run [-h] [-r RULES] [-v] [-f] [--no-error] [-t TAGS] [-e ENV] [--output {json}] [-b BRANCH] target\n\npositional arguments:\n  target                the target folder or git repo to run the compliance check on\n\noptions:\n  -h, --help            show this help message and exit\n  -r RULES, --rules RULES\n                        glob of rule files\n  -v, --verbose         increase output verbosity\n  -f, --hide-fail       hide failure out information\n  --no-error            dont exit 1 if security and fails are found\n  -t TAGS, --tags TAGS  project tags\n  -e ENV, --env ENV     environmental variables\n  --output {json}       output type\n  -b BRANCH, --branch BRANCH\n                        the branch to use if target is a git repo\n```\n\n## Rule file\n\nThe rules files are YAML files with the following format:\n```yaml\nname: sonarcube-setup   # Name your rule here\ndescription: |          # This is a verbose description\n  All projects must be registered in sonarcube\nimage: node:16          # Your steps are executed in this docker container\ntype: fail              # The type of rule info, warning, fail or security\ntags:                   # A list of tags. These then matched to the tags passed in from the command line for your execution.\n  - all\nsteps:                  # A list of commands executed. When a command has a non 0 response- the test is considered failed\n  - test -f sonar-project.properties\n```\n\n## Run using docker\n\nTo use the docker image of cmply it is important to pass through the hosts docker socket.\n\n```bash\ndocker run \\\n    -v //var/run/docker.sock:/var/run/docker.sock\n    -v ./rules:/opt/rules\n    -v ./target:/opt/target\n    -ti pselibas/cmply \\\n    run -r /opt/rules \\\n    /opt/target\n```\n\n',
    'author': 'Paul Selibas',
    'author_email': 'pselibas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pselibas/cmply',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

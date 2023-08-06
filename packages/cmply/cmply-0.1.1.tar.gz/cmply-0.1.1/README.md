# cmply

[![PyPI version](https://img.shields.io/pypi/v/cmply.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/cmply)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/cmply.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/cmply)
[![PyPI downloads](https://img.shields.io/pypi/dm/cmply.svg)](https://pypistats.org/packages/cmply)
[![Licence](https://img.shields.io/github/license/pselibas/cmply.svg)](LICENSE.txt)


## Installation

```bash
python3 -m pip install --upgrade cmply
```

## Introduction

Cmply is a tool used to run a set of rules against a repository.
The output will show the result of what rules fail or pass.
There is provision for different levels of failures. These levels are `info, warning, fail and security`.
The target can be a local folder or a git repository. 
If a git repository is specified, the local git is used with any configure authentication relative to the local system.

## Usage
```bash
usage: cmply run [-h] [-r RULES] [-v] [-f] [--no-error] [-t TAGS] [-e ENV] [--output {json}] [-b BRANCH] target

positional arguments:
  target                the target folder or git repo to run the compliance check on

options:
  -h, --help            show this help message and exit
  -r RULES, --rules RULES
                        glob of rule files
  -v, --verbose         increase output verbosity
  -f, --hide-fail       hide failure out information
  --no-error            dont exit 1 if security and fails are found
  -t TAGS, --tags TAGS  project tags
  -e ENV, --env ENV     environmental variables
  --output {json}       output type
  -b BRANCH, --branch BRANCH
                        the branch to use if target is a git repo
```

## Rule file

The rules files are YAML files with the following format:
```yaml
name: sonarcube-setup   # Name your rule here
description: |          # This is a verbose description
  All projects must be registered in sonarcube
image: node:16          # Your steps are executed in this docker container
type: fail              # The type of rule info, warning, fail or security
tags:                   # A list of tags. These then matched to the tags passed in from the command line for your execution.
  - all
steps:                  # A list of commands executed. When a command has a non 0 response- the test is considered failed
  - test -f sonar-project.properties
```

## Run using docker

To use the docker image of cmply it is important to pass through the hosts docker socket.

```bash
docker run \
    -v //var/run/docker.sock:/var/run/docker.sock
    -v ./rules:/opt/rules
    -v ./target:/opt/target
    -ti pselibas/cmply \
    run -r /opt/rules \
    /opt/target
```


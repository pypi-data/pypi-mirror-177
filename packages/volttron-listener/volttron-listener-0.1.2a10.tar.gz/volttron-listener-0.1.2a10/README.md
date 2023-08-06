![Passing?](https://github.com/eclipse-volttron/volttron-listener/actions/workflows/run-tests.yml/badge.svg)
[![pypi version](https://img.shields.io/pypi/v/volttron.svg)](https://pypi.org/project/volttron/)

The volttron-listener agent prints all message traffic across a VOLTTRON bus to standard out.

## Requirements

 - Python >= 3.8

## Installation

Create and activate a virtual environment.

```shell
python -m venv env
source env/bin/activate
```

Installing volttron-listener requires a running volttron instance.

```shell
pip install volttron

# Start platform with output going to volttron.log
volttron -vv -l volttron.log &
```

Install and start the volttron-listener.

```shell
vctl install volttron-listener --start
```

View the status of the installed agent

```shell
vctl status
```

## Development

Developing on this agent requires poetry 1.2.2 or greater be used.  One can install it from https://python-poetry.org/docs/#installation.  The VOLTTRON team prefers to have the python environments created within the project directory.  Execute
this command to make that behavior the default.

```shell
poetry config virtualenvs.in-project true
```

Clone the repository.

```shell
git clone https://github.com/eclipse-volttron/volttron-listener
```

Change to the repository directory and use poetry install to setup the environment.

```shell
cd volttron-listener
poetry install
```

### Building Wheel

To build a wheel from this project execute the following:

```shell
poetry build
```

The wheel and source distribution will be located in the ```./dist/``` directory.

### Bumping version number of project

To bump the version number of the project execute one of the following.

```shell
# patch, minor, major, prepatch, preminor, premajor, prerelease

# use patch
user@path$ poetry patch

# output
Bumping version from 0.2.0-alpha.0 to 0.2.0

# use prepatch
user@path$ poetry version prepatch

# output
Bumping version from 0.2.0 to 0.2.1-alpha.0
```

# Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.

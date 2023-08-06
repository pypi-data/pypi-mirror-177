# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['listener']

package_data = \
{'': ['*']}

install_requires = \
['volttron>=10.0.1a42,<11.0']

entry_points = \
{'console_scripts': ['volttron-listener-agent = listener.agent:main']}

setup_kwargs = {
    'name': 'volttron-listener',
    'version': '0.1.2a12',
    'description': 'None',
    'long_description': '![Passing?](https://github.com/eclipse-volttron/volttron-listener/actions/workflows/run-tests.yml/badge.svg)\n[![pypi version](https://img.shields.io/pypi/v/volttron.svg)](https://pypi.org/project/volttron/)\n\nThe volttron-listener agent prints all message traffic across a VOLTTRON bus to standard out.\n\n## Requirements\n\n - Python >= 3.8\n\n## Installation\n\nCreate and activate a virtual environment.\n\n```shell\npython -m venv env\nsource env/bin/activate\n```\n\nInstalling volttron-listener requires a running volttron instance.\n\n```shell\npip install volttron\n\n# Start platform with output going to volttron.log\nvolttron -vv -l volttron.log &\n```\n\nInstall and start the volttron-listener.\n\n```shell\nvctl install volttron-listener --start\n```\n\nView the status of the installed agent\n\n```shell\nvctl status\n```\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'Craig Allwardt',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-listener',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

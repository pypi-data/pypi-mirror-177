# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'volttron': 'tests/volttron',
 'volttron.historian.testing': 'tests/volttron/historian/testing'}

packages = \
['volttron', 'volttron.historian.base', 'volttron.historian.testing']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0',
 'volttron-testing>=0.3.1a16,<0.4.0',
 'volttron>=10.0.1a35,<11.0.0']

setup_kwargs = {
    'name': 'volttron-lib-base-historian',
    'version': '0.1.1a0',
    'description': 'None',
    'long_description': '[![ci](https://github.com/VOLTTRON/volttron-base-historian/workflows/ci/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-base-historian/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://VOLTTRON.github.io/volttron-lib-base-historian/)\n[![pypi version](https://img.shields.io/pypi/v/volttron-base-historian.svg)](https://pypi.org/project/volttron-lib-base-historian/)\n\nVOLTTRON base historian framework\n\n## Requirements\n\n - Python >= 3.8\n\n## Installation\n\nCreate and activate a virtual environment.\n\n```shell\npython -m venv env\nsource env/bin/activate\n```\n\nInstalling volttron-listener requires a running volttron instance.\n\n```shell\npip install volttron\n\n# Start platform with output going to volttron.log\nvolttron -vv -l volttron.log &\n```\n\nInstall and start the volttron-listener.\n\n```shell\nvctl install volttron-listener --start\n```\n\nView the status of the installed agent\n\n```shell\nvctl status\n```\n\n## Development\n\nDeveloping on this agent requires poetry 1.2.2 or greater be used.  One can install it from https://python-poetry.org/docs/#installation.  The VOLTTRON team prefers to have the python environments created within the project directory.  Execute\nthis command to make that behavior the default.\n\n```shell\npoetry config virtualenvs.in-project true\n```\n\nClone the repository.\n\n```shell\ngit clone https://github.com/eclipse-volttron/volttron-listener\n```\n\nChange to the repository directory and use poetry install to setup the environment.\n\n```shell\ncd volttron-listener\npoetry install\n```\n\n### Building Wheel\n\nTo build a wheel from this project execute the following:\n\n```shell\npoetry build\n```\n\nThe wheel and source distribution will be located in the ```./dist/``` directory.\n\n### Bumping version number of project\n\nTo bump the version number of the project execute one of the following.\n\n```shell\n# patch, minor, major, prepatch, preminor, premajor, prerelease\n\n# use patch\nuser@path$ poetry patch\n\n# output\nBumping version from 0.2.0-alpha.0 to 0.2.0\n\n# use prepatch\nuser@path$ poetry version prepatch\n\n# output\nBumping version from 0.2.0 to 0.2.1-alpha.0\n```\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.',
    'author': 'VOLTTRON Team',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-lib-base-historian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttron', 'volttron.historian.sql']

package_data = \
{'': ['*']}

install_requires = \
['volttron-lib-base-historian>=0.1.1a1,<0.2.0']

entry_points = \
{'console_scripts': ['volttron-sql-historian = '
                     'volttron.historian.sql.historian:main']}

setup_kwargs = {
    'name': 'volttron-lib-sql-historian',
    'version': '0.1.1a0',
    'description': 'None',
    'long_description': '\n[![ci](https://github.com/VOLTTRON/volttron-sql-historian/workflows/ci/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-sql-historian/actions?query=workflow%3Aci)\n[![pypi version](https://img.shields.io/pypi/v/volttron-sql-historian.svg)](https://pypi.org/project/volttron-lib-sql-historian/)\n\n\nGeneric SQL Historian library that can be used to implement a historian agent with a relational database backend. \nThis library cannot be installed as a VOLTTRON agent as is. Only a concrete database implementation package such as \n[sqlite-historian](https://github.com/eclipse-volttron/volttron-sqlitehistorian) that depends on this library can be \ninstalled as a VOLTTRON agent.\n\n\n## Requirements\n\n - Python >= 3.8\n\n## Installation\n\nThis library can be installed using ```pip install volttron-lib-sql-historian```. However this is not necessary. Any \nhistorian agent that uses this library will automatically install it as part of its installation. For example, \ninstalling [SQLiteHistorian](https://github.com/eclipse-volttron/volttron-sqlitehistorian) will automatically install \nvolttron-lib-sql-historian\n\n## Development\n\nDevelopment requires poetry 1.2.2 or greater be used.  \nOne can install it from https://python-poetry.org/docs/#installation.  The VOLTTRON team prefers to have the python \nenvironments created within the project directory.  Execute this command to make that behavior the default.\n\n```shell\npoetry config virtualenvs.in-project true\n```\n\nClone the repository.\n\n```shell\ngit clone https://github.com/eclipse-volttron/volttron-lib-sql-historian\n```\n\nChange to the repository directory and use poetry install to setup the environment.\n\n```shell\ncd volttron-lib-sql-historian\npoetry install\n```\n\n### Building Wheel\n\nTo build a wheel from this project execute the following:\n\n```shell\npoetry build\n```\n\nThe wheel and source distribution will be located in the ```./dist/``` directory.\n\n### Bumping version number of project\n\nTo bump the version number of the project execute one of the following.\n\n```shell\n# patch, minor, major, prepatch, preminor, premajor, prerelease\n\n# use patch\nuser@path$ poetry patch\n\n# output\nBumping version from 0.2.0-alpha.0 to 0.2.0\n\n# use prepatch\nuser@path$ poetry version prepatch\n\n# output\nBumping version from 0.2.0 to 0.2.1-alpha.0\n```\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'VOLTTRON',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-lib-sql-historian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['historian', 'historian.sql']

package_data = \
{'': ['*']}

install_requires = \
['volttron-lib-base-historian>=0.1.1a3,<0.2.0']

setup_kwargs = {
    'name': 'volttron-lib-sql-historian',
    'version': '0.1.1a2',
    'description': 'None',
    'long_description': '\n[![ci](https://github.com/VOLTTRON/volttron-sql-historian/workflows/ci/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-sql-historian/actions?query=workflow%3Aci)\n[![pypi version](https://img.shields.io/pypi/v/volttron-sql-historian.svg)](https://pypi.org/project/volttron-lib-sql-historian/)\n\nGeneric SQL Historian library that can be used to implement a historian agent with a relational database backend. \nThis library cannot be installed as a VOLTTRON agent as is. Only a concrete database implementation package such as \n[sqlite-historian](https://github.com/eclipse-volttron/volttron-sqlitehistorian) that depends on this library can be \ninstalled as a VOLTTRON agent.\n\n## Requirements\n\n - Python >= 3.8\n\n## Installation\n\nThis library can be installed using ```pip install volttron-lib-sql-historian```. However, this is not necessary. Any \nhistorian agent that uses this library will automatically install it as part of its installation. For example, \ninstalling [SQLiteHistorian](https://github.com/eclipse-volttron/volttron-sqlitehistorian) will automatically install \nvolttron-lib-sql-historian\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\nTo create a new relational database based historian by extending this library, subclass \n[DBDriver](https://github.com/eclipse-volttron/volttron-lib-sql-historian/blob/develop/src/historian/sql/basedb.py#L79).\nThe subclass should be in a module historian.<database_type>.<database_type>functs.py for it to be dynamically loaded \nby the base DBDriver. Please refer to [SQLiteHistorian](https://github.com/eclipse-volttron/volttron-sqlitehistorian) as \nan example\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'VOLTTRON',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-lib-sql-historian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

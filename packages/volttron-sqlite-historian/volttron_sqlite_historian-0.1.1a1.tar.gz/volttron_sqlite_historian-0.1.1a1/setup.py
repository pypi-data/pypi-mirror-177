# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttron', 'volttron.historian.sqlite']

package_data = \
{'': ['*']}

install_requires = \
['volttron-lib-sql-historian>=0.1.1a2,<0.2.0']

entry_points = \
{'console_scripts': ['volttron-sqlite-historian = '
                     'volttron.historian.sql.historian:main']}

setup_kwargs = {
    'name': 'volttron-sqlite-historian',
    'version': '0.1.1a1',
    'description': 'None',
    'long_description': '\n[![ci](https://github.com/VOLTTRON/volttron-sqlite-historian/workflows/ci/badge.svg)](https://github.com/VOLTTRON/volttron-sqlite-historian/actions?query=workflow%3Aci)\n[![pypi version](https://img.shields.io/pypi/v/volttron-sqlite-historian.svg)](https://pypi.org/project/volttron-sqlite-historian/)\n\nVOLTTRON historian agent that stores data into a SQLite database\n\n\n## Requirements\n\n - Python >= 3.8\n\n## Installation\n\n1. Create and activate a virtual environment.\n\n```shell\npython -m venv env\nsource env/bin/activate\n```\n\n2. Installing volttron-sqlite-historian requires a running volttron instance.\n\n```shell\npip install volttron\n\n# Start platform with output going to volttron.log\nvolttron -vv -l volttron.log &\n```\n\n3. Create a agent configuration file\n\nSQLite historian supports two parameters\n\nconnection - This is a mandatory parameter with type indicating the type of sql historian (i.e. sqlite) and params \n             containing the path the database file.\n\ntables_def - Optional parameter to provide custom table names for topics, data, and metadata.\n\nExample:\n\nJSON format :\n\n    {\n        "connection": {\n            # type should be sqlite\n            "type": "sqlite",\n            "params": {\n                "database": "data/historian.sqlite",\n            }\n        }\n        "tables_def":  {\n            # prefix for data, topics, and (in version < 4.0.0 metadata tables)\n            # default is ""\n            "table_prefix": "",\n            # table name for time series data. default "data"\n            "data_table": "data",\n            # table name for list of topics. default "topics"\n            "topics_table": "topics",\n            # table name mapping topic to metadata. default "meta"\n            # In sqlhistorian version >= 4.0.0 metadata is stored in topics table\n            "meta_table": "meta"\n        }\n    }\n\n4. Install and start the volttron-sqlite-historian.\n\n```shell\nvctl install volttron-sqlite-historian --agent-config <path to configuration> --start\n```\n\n5. View the status of the installed agent\n\n```shell\nvctl status\n```\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'VOLTTRON Team',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VOLTTRON/volttron-sqlite-historian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['madmigration',
 'madmigration.basemigration',
 'madmigration.config',
 'madmigration.db_init',
 'madmigration.db_operations',
 'madmigration.mongodb',
 'madmigration.mssql',
 'madmigration.mysqldb',
 'madmigration.postgresqldb',
 'madmigration.postgresqldb.schemas',
 'madmigration.scripts',
 'madmigration.utils']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.8.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'mysql>=0.0.3,<0.0.4',
 'psycopg2>=2.9.5,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pymongo>=4.3.2,<5.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'regex>=2022.10.31,<2023.0.0',
 'sqlalchemy-utils>=0.38.3,<0.39.0',
 'sqlalchemy>=1.4.44,<2.0.0']

entry_points = \
{'console_scripts': ['madmigration = madmigration.run:run']}

setup_kwargs = {
    'name': 'madmigration',
    'version': '0.1.28',
    'description': 'Mad Migration',
    'long_description': 'None',
    'author': 'Hasan',
    'author_email': 'hasan.aleeyev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

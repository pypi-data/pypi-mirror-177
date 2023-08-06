# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kclii',
 'kclii.consts',
 'kclii.database',
 'kclii.envs',
 'kclii.error',
 'kclii.helper',
 'kclii.modules',
 'kclii.modules.profiles',
 'kclii.scripts']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.8.1,<2.0.0',
 'load-dotenv>=0.1.0,<0.2.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'sqlalchemy>=1.4.43,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['k = kclii.main:app', 'kinit = kclii.init:main']}

setup_kwargs = {
    'name': 'kclii',
    'version': '0.1.10',
    'description': 'CLI multipurpose.',
    'long_description': '# K CLI\n\nCreate migration\n\nalembic revision --autogenerate -m "init"\n\nUpgrade to the latest version\n\nalembic upgrade head \n\nDowngrade\n\nalembic downgrade base\n\ncheck history\n\nalembic history',
    'author': 'Andres Garcia',
    'author_email': 'jose.andres.gm29@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

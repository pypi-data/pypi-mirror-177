# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lr_etl',
 'lr_etl.Config',
 'lr_etl.Libs',
 'lr_etl.Libs.db',
 'lr_etl.Models',
 'lr_etl.Models.db',
 'lr_etl.Models.entities',
 'lr_etl.Steps',
 'lr_etl.use_cases']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.4.1,<3.0.0',
 'pandas>=1.5.1,<2.0.0',
 'paramiko>=2.12.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'sqlalchemy-utils>=0.38.3,<0.39.0',
 'sqlalchemy>=1.4.44,<2.0.0']

setup_kwargs = {
    'name': 'lr-etl',
    'version': '0.0.3',
    'description': '',
    'long_description': '',
    'author': 'FernandoEmerson',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

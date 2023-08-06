# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_mssql',
 'target_mssql.tests',
 'target_mssql.tests.samples',
 'target_mssql.tests.samples.aapl',
 'target_mssql.tests.samples.sample_tap_countries']

package_data = \
{'': ['*'],
 'target_mssql.tests': ['data_files/*'],
 'target_mssql.tests.samples.sample_tap_countries': ['schemas/*']}

install_requires = \
['pymssql>=2.2.5', 'requests>=2.25.1,<3.0.0', 'singer-sdk==0.13.0']

entry_points = \
{'console_scripts': ['target-mssql = target_mssql.target:Targetmssql.cli']}

setup_kwargs = {
    'name': 'target-mssql',
    'version': '0.0.1',
    'description': '`target-mssql` is a Singer target for mssql, built with the Meltano SDK for Singer Targets.',
    'long_description': 'None',
    'author': 'Henning Holgersen',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

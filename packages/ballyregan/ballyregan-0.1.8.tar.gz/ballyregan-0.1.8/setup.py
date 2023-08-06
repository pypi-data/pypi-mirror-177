# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ballyregan',
 'ballyregan.core',
 'ballyregan.models',
 'ballyregan.providers',
 'cli',
 'cli.core']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=15.1.1,<16.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=8.1.3,<9.0.0',
 'gevent>=22.10.1,<23.0.0',
 'grequests>=0.6.0,<0.7.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.5.0,<2.0.0',
 'prettytable>=3.4.1,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pythonping>=1.1.4,<2.0.0',
 'requests[socks]>=2.28.1,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0',
 'urllib3[socks]>=1.26.12,<2.0.0']

entry_points = \
{'console_scripts': ['ballyregan = cli.app:run']}

setup_kwargs = {
    'name': 'ballyregan',
    'version': '0.1.8',
    'description': 'Tool for fetching online proxies easily and efficiently.',
    'long_description': None,
    'author': 'idandaniel',
    'author_email': 'idandaniel12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

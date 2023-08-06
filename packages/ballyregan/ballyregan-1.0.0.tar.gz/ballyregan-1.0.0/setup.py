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
    'version': '1.0.0',
    'description': 'Find fetch & validate free proxies fast.',
    'long_description': '[![Python](https://img.shields.io/pypi/pyversions/ballyregan.svg)](https://badge.fury.io/py/ballyregan)\n[![PyPI](https://badge.fury.io/py/ballyregan.svg)](https://badge.fury.io/py/ballyregan)\n[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-yellow)](https://opensource.org/licenses/Apache-2.0)\n\n# Ballyregan 🔷\n## Find fetch & validate free proxies fast.\n\n<br>\n\n## How does it work?\nBallyregan fetches the proxies from  list of built in providers.\n> Provider - any website that serves free proxy lists (e.g https://free-proxy-list.net).\n\nYou can write and append your own custom providers and pass it to the ProxyFetcher class as attribute. <br>\n> **Note** <br>\n> Every custom proxy provider must implement the [IProxyProvider](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/providers/interface.py) base interface.\n\n<br>\n\n## Behind the scenes\nBallyregan uses [greenlets](https://greenlet.readthedocs.io/en/latest). <br>\nFetching a proxy is an [IO bound operation](https://en.wikipedia.org/wiki/I/O_bound) which depends on network, <br>\nand greenlets provide concurrency, so by using them we are able validate thousands of proxies efficiently. <br>\n\n<br>\n\n## Install\n\n```sh\npip install ballyregan\n```\n\n## Usage\n\n### Package 📦\n\n#### Create a fetcher instance\n```python\nfrom ballyregan import ProxyFetcher\n\n# Setting the debug mode to True, defaults to False\nfetcher = ProxyFetcher(debug=True)\n```\n\n#### Get one proxy\n```python\nproxy = fetcher.get_one()\nprint(proxy)\n```\n\n#### Get multiple proxies\n```python\nproxies = fetcher.get(limit=4)\nprint(proxies)\n```\n\n#### Get proxies by filters\n```python\nfrom ballyregan.models import Protocols, Anonymities\n\nproxies = fetcher.get(\n  limit=4,\n  protocols=[Protocols.HTTPS, Protocols.SOCKS5],\n  anonymities=[Anonymities.ELITE]\n)\nprint(proxies)\n```\n\n### CLI 💻\n\n#### Get all proxies\n```sh\nballyregan get --all\n```\n\n#### Get one proxy\n```sh\nballyregan get --all\n```\n\n#### Use debug mode\n```sh\nballyregan --debug get [OPTIONS]\n```\n\n#### Format output to json\n```sh\nballyregan get -o json\n```\n\n#### Get proxies by limit\n```sh\nbellyregan get -l 4\n```\n\n#### Get proxies by filters\n```sh\nbellyregan get -l 4 -p https -p socks5 -a elite\n```\n\n---\n\n## Author\n\n👤 **Idan Daniel**\n\n* Github: [@idandaniel](https://github.com/idandaniel)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\n## 📝 License\n\nCopyright © 2022 [Idan Daniel](https://github.com/idandaniel).<br />\nThis project is [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) licensed.\n\n',
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

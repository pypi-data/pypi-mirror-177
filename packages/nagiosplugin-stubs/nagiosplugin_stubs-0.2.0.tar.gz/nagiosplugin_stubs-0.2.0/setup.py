# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nagiosplugin-stubs']

package_data = \
{'': ['*'], 'nagiosplugin-stubs': ['examples/*', 'platform/*']}

install_requires = \
['typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'nagiosplugin-stubs',
    'version': '0.2.0',
    'description': 'Type stubs for the nagiosplugin package.',
    'long_description': 'nagiosplugin-stubs\n==================\n\nType stubs for the nagiosplugin package.\n\nOther stub packages\n\n* https://github.com/lxml/lxml-stubs\n* https://github.com/tk0miya/docutils-stubs\n',
    'author': 'Josef Friedrich',
    'author_email': 'josef@friedrich.rocks',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Josef-Friedrich/nagiosplugin-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

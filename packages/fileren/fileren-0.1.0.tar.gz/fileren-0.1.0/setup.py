# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fileren']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['fileren = fileren.main:main']}

setup_kwargs = {
    'name': 'fileren',
    'version': '0.1.0',
    'description': 'Simple tool for renaming files in a directory',
    'long_description': '# Fileren\n\nSimple tool for renaming files in a directory\n\n![How to use gif](assets/how_to_use.gif)\n\n## Usage\n\nTo run the program, simply run the following command:\n\n```shell\nfileren\n```\n\nOr run command with arguments:\n\n```shell\nfileren --path {path_to_directory} --regex {regex} --new_string {new_string}\n```\n',
    'author': 'Mikołaj Badyl',
    'author_email': 'contact@hawier.dev',
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

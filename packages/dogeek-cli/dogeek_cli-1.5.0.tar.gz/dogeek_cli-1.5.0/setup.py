# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dogeek_cli', 'dogeek_cli.subcommands']

package_data = \
{'': ['*'], 'dogeek_cli': ['templates/plugin/*']}

install_requires = \
['Mako>=1.2.1,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'cryptography[ssh]>=37.0.4,<38.0.0',
 'gitignore-parser>=0.0.8,<0.0.9',
 'pick>=1.4.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.6.1,<0.7.0',
 'xdgconfig>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['cli = dogeek_cli.app:main']}

setup_kwargs = {
    'name': 'dogeek-cli',
    'version': '1.5.0',
    'description': 'Interactive CLI to store scripts into',
    'long_description': 'None',
    'author': 'Dogeek',
    'author_email': 'simon.bordeyne@gmail.com',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotils', 'spotils.dev', 'spotils.helpers', 'spotils.utils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.3,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'mergedeep>=1.3.4,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=12.6.0,<13.0.0',
 'schedule>=1.1.0,<2.0.0',
 'spotipy>=2.21.0,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['spotils = spotils.cli:app']}

setup_kwargs = {
    'name': 'spotils',
    'version': '0.1.0',
    'description': 'A few utilities for providing a smoother Spotify experience.',
    'long_description': '# spotify\nA few utilities for providing a smoother Spotify experience.\n',
    'author': 'Qwerty-133',
    'author_email': '74311372+Qwerty-133@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Qwerty-133/spotils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

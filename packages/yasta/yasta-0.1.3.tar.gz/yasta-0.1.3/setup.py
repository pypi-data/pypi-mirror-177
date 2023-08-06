# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yasta']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['yasta = yasta.yasta:app']}

setup_kwargs = {
    'name': 'yasta',
    'version': '0.1.3',
    'description': 'A modern task runner.',
    'long_description': "# Yasta\n\n![Yasta logo](https://i.imgur.com/MGw6TNI_d.webp?maxwidth=760)\n\nYasta is a modern task runner written in Python, it's also what we call microbus drivers in Egypt! 🚐\n\nYasta makes running and managing your tasks a breeze! 🌬️\n\n# How to install\n\n```\npip install yasta\n```\n\n# How to use\n\nYasta consists of 5 commands\n\n1. init (initializes a pyproject.toml file with a test command)\n2. add (adds a task to the list of tasks)\n3. delete (deletes a task from the list of tasks)\n4. show (shows the tables of tasks)\n5. run (runs a task)\n\nYou can know more about the commands and flags by running\n\n```\nyasta --help\n```\n\n# Example\n\n![Yasta init, adding and running tasks](https://i.imgur.com/Y55f9AN_d.webp?maxwidth=1520)\n\n![Yasta force running commands, ignoring failed tasks](https://i.imgur.com/FsOrx3X_d.webp?maxwidth=1520)\n",
    'author': 'Adham Salama',
    'author_email': 'adhamsalama@zohomail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adhamsalama/yasta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djtodo_cli', 'djtodo_cli.djtodo']

package_data = \
{'': ['*']}

modules = \
['File', 'module']
entry_points = \
{'console_scripts': ['djtodo = djtodo_cli.djtodo.djtodo:cli']}

setup_kwargs = {
    'name': 'djtodo-cli',
    'version': '0.1.3',
    'description': '',
    'long_description': '# djtodo-cli\n\ndjtodo-cli is a CLI todo application.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install djtodo-cli.\n\n```bash\npip install djtodo-cli\n```\n\n## Usage\n\n```add\ndjtodo add <task>\n```\n>add task\n\n```list\ndjtodo list\n```\n>print list of task\n\n```remove\ndjtodo remove <number>\n```\n> remove task\n\n```done\ndjtodo done <number>\n```\n>mark task as done\n\n```search\ndjtdo search <task>\n```\n>search for the task\n \n  \n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first\nto discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n\n\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dongjin2008/djtodo',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

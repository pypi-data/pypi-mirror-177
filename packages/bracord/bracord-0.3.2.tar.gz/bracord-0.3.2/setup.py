# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bracord', 'bracord.cli']

package_data = \
{'': ['*']}

install_requires = \
['disnake>=2.7.0,<3.0.0',
 'flake8>=5.0.4,<6.0.0',
 'isort>=5.10.1,<6.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['bracord = disnake.ext.bracord.entry:main']}

setup_kwargs = {
    'name': 'bracord',
    'version': '0.3.2',
    'description': 'A Disnake framework written in Python that speeds the development of Discord bots.',
    'long_description': "# Bracord\nA [Disnake](https://github.com/DisnakeDev/Disnake) framework written in Python that speeds the development of Discord bots.\n\nBracord is a combination of a command line tool and ready-to-go cogs that might come useful when developing quick Discord bots.\n\n**Table of Contents**\n- [Installation](#installation)\n- [Usage](#usage)\n\n## Installation\n\nYou can install Bracord using `pip`.\n\n```bash\n$ pip3 install bracord\n```\n\n## Usage\n\n### Project Initialization\nFirst, you will need to initialize a Bracord project. You can do so with the following command:\n\n```bash\n$ bracord init\n```\n\nThis will start asking for information related to your bot and then create all necessary files in the current directory.\n\n### Cog Creation\nTo create and register a cog, you can use the `cog` command:\n\n```bash\n$ bracord cog\n```\n\nThis will ask you for the cog's name and will create it and load it whenever when the bot is started.\n",
    'author': 'MrFellox',
    'author_email': 'jfernandohernandez28@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mrfellox/bracord',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

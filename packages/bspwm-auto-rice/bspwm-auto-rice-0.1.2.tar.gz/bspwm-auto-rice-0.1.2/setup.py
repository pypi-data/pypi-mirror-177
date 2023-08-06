# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bspwm_auto_rice']

package_data = \
{'': ['*']}

install_requires = \
['pywal>=3.3.0,<4.0.0', 'rich>=12.6.0,<13.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['bspar = bspwm_auto_rice.bspar:cli']}

setup_kwargs = {
    'name': 'bspwm-auto-rice',
    'version': '0.1.2',
    'description': '',
    'long_description': '## bspwm auto rice [bspar]\nan automatice ricing script for bspwm (my dots)\n\nONLY WORKS ON ARCH BASED DISTROS\n\n## demo\n[Demo](https://i.imgur.com/VBXp4yK.mp4)\n\n## Installation\n```pip install bspwm-auto-rice```\n\n## Usage\nfor help:\n```bspar --help```\nand \n```bspar <command> --help```\nexample:\n```bspar set --help```',
    'author': 'AbdelrhmanNile',
    'author_email': 'abdelrhmannile@gmail.com',
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

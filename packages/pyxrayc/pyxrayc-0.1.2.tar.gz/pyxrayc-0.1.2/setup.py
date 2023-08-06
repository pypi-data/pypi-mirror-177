# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxrayc', 'pyxrayc.cli']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pyxrayc = pyxrayc.cli.main:app']}

setup_kwargs = {
    'name': 'pyxrayc',
    'version': '0.1.2',
    'description': 'CLI utility for managing Xray servers with ease on Linux, written in Python.',
    'long_description': '<div align="center">\n<h1><a href="https://github.com/PlumaCompanyLtd/PyXrayC"><b>PyXrayC</b></a></h1>\n<a href="https://github.com/PlumaCompanyLtd/PyXrayC/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/PlumaCompanyLtd/PyXrayC/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python">\n</a>\n<a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/static/v1?label=code%20style&message=black&color=black&style=flat" alt="Code Style: black">\n</a>\n<a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit">\n</a>\n</div>\n\n## Table of Contents\n\n- [Introduction](#introduction)\n- [Features](#features)\n- [Requirements](#requirements)\n- [Setup](#setup)\n- [Usage](#usage)\n- [License](#license)\n\n## Introduction\n\n_PyXrayC_ is a CLI tool built with Python and [Typer] library that helps you to manage your [Xray] VPN server\'s configurations\non Linux OS with minimum effort from you!\n\n## Features\n\n- Installable via `pip`\n- Fully type hinted and extensible code base.\n- Public API for other Python programmers that want to use specific features in their code.\n- Optional shell autocompletion.\n- Add, view or delete users to/from your config file.\n- Set limits on number of devices a user can connect from.\n\n## Requirements\n\n- A Linux distribution with [Xray] VPN server installed on it.\n- Python 3.8 or higher.\n\n## Setup\n\n## Usage\n\n## License\n\nThis project is licensed under the terms of the [GPL-3.0] licence.\n\n<p align="center">&mdash; ⚡ &mdash;</p>\n\n<!-- Links -->\n\n[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU General Public License v3.0"\n[typer]: https://github.com/tiangolo/typer "Typer, build great CLIs. Easy to code. Based on Python type hints."\n[xray]: https://github.com/XTLS "Project X"\n',
    'author': 'Seyed',
    'author_email': 'pyseyed@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PlumaCompanyLtd/PyXrayC',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invisible_backdoor_detector']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['invisible-backdoor-detector = '
                     'invisible_backdoor_detector.main:app']}

setup_kwargs = {
    'name': 'invisible-backdoor-detector',
    'version': '0.1.0',
    'description': 'A simple tool to spot and remove Bidi characters that could lead to an invisible backdoor',
    'long_description': '# Invisible Backdoor Detector\n<p align="center">\n  <img id="header" src="https://raw.githubusercontent.com/cybersecsi/invisible-backdoor-detector/main/docs/logo.png" />\n</p>\n\n<p align="center">\n  <a href="https://github.com/cybersecsi/invisible-backdoor-detector/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>\n  <a href="https://github.com/cybersecsi/invisible-backdoor-detector/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>\n</p>\n\n\n**Invisible Backdoor Detector** is a little *Python* script that allows you to **spot** and **remove** Bidi characters that could lead to an **invisible backdoor**. If you don\'t know what that is you should check the related paragraph.\n\n## Table of Contents\n  - [What is an Invisible Backdoor](#what-is-an-invisible-backdoor)\n  - [Install](#install)\n  - [Usage](#usage)\n  - [Examples](#examples)\n  - [Contributions](#contributions)\n  - [Credits](#credits)\n  - [License](#license)\n\n## What is an Invisbile Backdoor\nAn Invisible Backdoor is exactly what you think: a backdoor that you cannot see! It was described by *Wolfgang Ettlinger* at *Certitude* in [this blog post](https://certitude.consulting/blog/en/invisible-backdoor/). It leverages the presence of Unicode characters (Bidi characters) which behaves like normal spaces. In conjunction with the Javascript object destructuring those characters may allow an attacker to introduce a backdoor into an open-source project without anyone noticing it. Check out the blog post for more info.\n\n## Install\nYou can easily install it by running:\n```\npip install invisible-backdoor-detector\n```\n\n## Usage\n```\ninvisible-backdoor-detector -h\n```\n\n```\n Usage: invisible-backdoor-detector [OPTIONS] PATH                                                                          \n                                                                                                                            \n╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ *    path      TEXT  Path of the folder to check [default: None] [required]                                              │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --remove  -r        Remove the Bidi characters found                                                                     │\n│ --help    -h        Show this message and exit.                                                                          │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n\n```\n\n## Example\nThe *example* folder provides a working example of an invisible backdoor in Node.js, you may test the script on that folder. \nIf you want to try out the backdoor you can add the following parameter to the query string:\n```\n%E3%85%A4=<any command>\n```\n\n## Contributions\nEveryone is invited to contribute!\nIf you are a user of the tool and have a suggestion for a new feature or a bug to report, please do so through the issue tracker.\n\n## Credits\nDeveloped by Angelo Delicato [@SecSI](https://secsi.io)\n\n## License\n*invisible-backdoor-detector* is released under the [MIT LICENSE](https://github.com/cybersecsi/invisible-backdoor-detector/blob/main/LICENSE.md)\n\n',
    'author': 'SecSI',
    'author_email': 'dev@secsi.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

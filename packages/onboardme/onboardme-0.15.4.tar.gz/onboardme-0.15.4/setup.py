# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onboardme']

package_data = \
{'': ['*'],
 'onboardme': ['config/*',
               'config/firewall/*',
               'config/firewall/ufw/*',
               'config/terminal.sexy/*']}

install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'rich>=12.6.0,<13.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['onboardme = onboardme:main']}

setup_kwargs = {
    'name': 'onboardme',
    'version': '0.15.4',
    'description': 'An onboarding tool to install dot files and packages including a default mode with sensible defaults to run on most Debian/macOS machines.',
    'long_description': '## ☁️  onboard**me** 💻\n\n[![./docs/onboardme/screenshots/help_text.svg alt=\'screenshot of full output of onboardme --help](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)\n\nThis is a project to store config files, as well as programatically install core packages across several package managers that we need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping we\'d remember why it was there later, so this is now a renewed effort in remembering all the thing™️s, and automating as much as possible. The idea is that it\'s faster, smaller, and easier to configure than it\'s ansible equivalent.\n\nHere\'s an example of the terminal after the script has run:\n\n[<img alt="screenshot of terminal after runnign onboardme. includes colortest-256, powerline prompt, icons for files in ls output, and syntax highlighting examples with cat command." width="750" src="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png">](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png)\n\n\n## Quick Start\nThe quickest way to get started on a fresh macOS or Debian OS is:\n```bash\n# this will download setup.sh to your current directory and run it\n/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh)"\n\n# this will display the help for the onboardme cli\nonboardme --help\n```\nYou can also read more in depth [Getting Started docs](https://jessebot.github.io/onboardme/onboardme/getting-started) 💙!\n\n\n#### More Docs\nWe\'ve recently setup a justthedocs page [here](https://jessebot.github.io/onboardme/).\n\n### Upgrading\nIf you\'re on python3.11.0 or later, you should be able to do:\n```bash\npip3.11 install --upgrade onboardme\n```\n\n## Features\nMade for the following OS (lastest stable):\n\n[![made-for-macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://wikiless.org/wiki/MacOS?lang=en)\n[![made-for-debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/)\n[![made-for-ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)\n\nOptimized for:\n\n[![made-with-for-vim](https://img.shields.io/badge/VIM-%2311AB00.svg?&style=for-the-badge&logo=vim&logoColor=white)](https://www.vim.org/)\n[![made-with-python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)\n[![made-with-bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=GNU%20Bash&logoColor=white)](https://www.gnu.org/software/bash/)\n\nAnd built using these great projects. Please go check them out:\n\n[<img src="https://github.com/textualize/rich/raw/master/imgs/logo.svg" alt="rich python library logo with with yellow snake" width="200">](https://github.com/Textualize/rich/tree/master)\n[<img src="https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/images/nerd-fonts-logo.svg" width="140" alt="nerd-fonts: Iconic font aggregator, collection, and patcher">](https://www.nerdfonts.com/)\n- [powerline](https://powerline.readthedocs.io/en/master/overview.html)\n\n## Status\n\n🎉 Active project! Currently in later alpha :D (*But not yet stable. There be 🐛.*)\n\nPlease report 🐛 in the GitHub issues, and we will collect them,\nand release them into the wild, because we are vegan and nice.\n(Kidding, we will help! 😌)\n\nWe love contributors! Feel free to open a pull request, and we will review it asap! :)\n\n:star: If you like this project, please star it to help us keep motivated :3\n\n## Collaborators\n\n<!-- readme: collaborators -start -->\n<table>\n<tr>\n    <td align="center">\n        <a href="https://github.com/jessebot">\n            <img src="https://avatars.githubusercontent.com/u/2389292?v=4" width="100;" alt="jessebot"/>\n            <br />\n            <sub><b>JesseBot</b></sub>\n        </a>\n    </td>\n    <td align="center">\n        <a href="https://github.com/cloudymax">\n            <img src="https://avatars.githubusercontent.com/u/84841307?v=4" width="100;" alt="cloudymax"/>\n            <br />\n            <sub><b>Max!</b></sub>\n        </a>\n    </td></tr>\n</table>\n<!-- readme: collaborators -end -->\n\n## Shameless plugs for other projects\nLooking for a project to get running on a machine that has no OS at all?\nCheck out [pxeless](https://github.com/cloudymax/pxeless).\n\nLooking for a project to get started with self hosting k8s stuff?\nCheck out [smol k8s lab](https://github.com/jessebot/smol_k8s_lab).\n',
    'author': 'Jesse Hitch',
    'author_email': 'jessebot@linux.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/jessebot/onboardme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

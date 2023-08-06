# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['browniebroke_utils']

package_data = \
{'': ['*'],
 'browniebroke_utils': ['templates/prettier/*', 'templates/pywatchers/*']}

install_requires = \
['xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['pych-prettier = browniebroke_utils.setup_prettier:main',
                     'pych-pywatchers = '
                     'browniebroke_utils.setup_pywatchers:main']}

setup_kwargs = {
    'name': 'browniebroke-utils',
    'version': '0.1.0',
    'description': 'A collections of small scripts.',
    'long_description': '# Browniebroke Utils\n\n<p align="center">\n  <a href="https://github.com/browniebroke/browniebroke-utils/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/browniebroke/browniebroke-utils/CI/main?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://codecov.io/gh/browniebroke/browniebroke-utils">\n    <img src="https://img.shields.io/codecov/c/github/browniebroke/browniebroke-utils.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/browniebroke-utils/">\n    <img src="https://img.shields.io/pypi/v/browniebroke-utils.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/browniebroke-utils.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/browniebroke-utils.svg?style=flat-square" alt="License">\n</p>\n\nA collections of small scripts.\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install browniebroke-utils`\n\n## Usage\n\nThis tool provides a few random scripts I use in my day to day work.\n\n### `pych-prettier`\n\nConfigure [Prettier](https://prettier.io/) as file watcher in the current PyCharm project. This is done by editing the appropriate files in the `.idea` folder.\n\n### `pych-pywatchers`\n\nSetup a few Python-related linting tools as file watchers in the current PyCharm project:\n\n- Black\n- isort\n- pyupgrade\n\nThis is done by editing the appropriate files in the `.idea` folder.\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n    <tr>\n      <td align="center" valign="top" width="14.28%"><a href="https://browniebroke.com/"><img src="https://avatars.githubusercontent.com/u/861044?v=4?s=80" width="80px;" alt="Bruno Alla"/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/browniebroke-utils/commits?author=browniebroke" title="Code">💻</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/browniebroke/browniebroke-utils/commits?author=browniebroke" title="Documentation">📖</a></td>\n    </tr>\n  </tbody>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Copier](https://copier.readthedocs.io/) and the\n[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)\nproject template.\n',
    'author': 'Bruno Alla',
    'author_email': 'alla.brunoo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/browniebroke/browniebroke-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toyotama',
 'toyotama.ad',
 'toyotama.connect',
 'toyotama.crypto',
 'toyotama.elf',
 'toyotama.pwn',
 'toyotama.terminal',
 'toyotama.util',
 'toyotama.web']

package_data = \
{'': ['*']}

install_requires = \
['gmpy2>=2.1.2,<3.0.0', 'r2pipe>=1.6.5,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'toyotama',
    'version': '0.9.8',
    'description': 'Python library for CTF.',
    'long_description': '\n# Toyotama\n[![CodeFactor](https://www.codefactor.io/repository/github/laika/toyotama/badge)](https://www.codefactor.io/repository/github/laika/toyotama)\n![](https://img.shields.io/badge/Python-3.9.*-1c0c28)\n[![](https://img.shields.io/pypi/v/toyotama?color=1c0c28&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/toyotama/)  \n\n\nCTF Library\n\n## Notice\n* No document. (for now)\n\n## Install \n```\npip install toyotama\n```\n## Uninstall\n```\npip uninstall toyotama\n```\n\n\n## Examples\n* Connect\n[![asciicast](https://asciinema.org/a/uNEjp2IiGu0JKJxJlyYnWabRm.svg)](https://asciinema.org/a/uNEjp2IiGu0JKJxJlyYnWabRm)\n\n* padding\\_oracle\\_attack\n[![asciicast](https://asciinema.org/a/j1hYdI966cmPknuGpBUMVxkAv.svg)](https://asciinema.org/a/j1hYdI966cmPknuGpBUMVxkAv)\n\n\n\n\n\n\n',
    'author': 'Laika',
    'author_email': 'laika@albina.cc',
    'maintainer': 'Laika',
    'maintainer_email': 'laika@albina.cc',
    'url': 'https://github.com/Laika/Toyotama',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

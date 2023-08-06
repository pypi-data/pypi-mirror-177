# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kithon', 'kithon.commands']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<4.0.0', 'PyYaml>=5.4.0', 'typer>=0.4.0,<0.5.0']

extras_require = \
{':extra == "add-langs" or extra == "all"': ['hy<2.0'],
 ':extra == "pyx" or extra == "all"': ['packed>=0.2,<0.3'],
 'add-langs': ['coconut>=1.6.0,<2.0.0'],
 'all': ['coconut>=1.6.0,<2.0.0',
         'pexpect>=4.8.0,<5.0.0',
         'ptpython>=3.0.20,<4.0.0',
         'watchdog>=2.1.7,<3.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-material>=8.1.4,<9.0.0',
         'mdx-include>=1.4.1,<2.0.0'],
 'repl': ['pexpect>=4.8.0,<5.0.0', 'ptpython>=3.0.20,<4.0.0'],
 'watch': ['watchdog>=2.1.7,<3.0.0']}

entry_points = \
{'console_scripts': ['kithon = kithon.commands:kithon']}

setup_kwargs = {
    'name': 'kithon',
    'version': '0.6.0',
    'description': 'transpiler python into other languages',
    'long_description': '[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/alploskov/kithon/blob/master/LICENSE.txt) <a href="https://pypi.org/project/kithon" target="_blank"> <img src="https://img.shields.io/pypi/v/kithon?color=%2334D058&label=pypi%20package" alt="Package version"></a> ![lines of code](https://tokei.rs/b1/github/alploskov/kithon)\n\n**Kithon** is universal python transpiler for speedup python programs and use python in other platform, such as browser or game engines, it focused on generating human readable code and integration with tools of target languages including cli and libraries\n\n**[Try out the web demo](https://alploskov.github.io/kithon-site/demo/)**\n\nQuick start\n------------\nFirst, you install it:\n\n```text\n$ pip install kithon[all]\n```\n\nThen, you translate your code to target language, in this example JavaSctipt\n\n```text\n$ kithon gen --to js hello_world.py\n```\n\nOr translate and run resulting code\n\n```text\n$ kithon run --to go hello_world.py\n```\nIt should be clear what to do. If not, ask us in our [Telegram chat](https://t.me/kithon).\n\nHow to Contribute\n-----------------\n\nFirst, install `python>=3.9`, `poetry`\n',
    'author': 'Aleksey Ploskov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alploskov/kithon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<3.11',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialog_reflection', 'dialog_reflection.lang', 'dialog_reflection.lang.ja']

package_data = \
{'': ['*']}

install_requires = \
['katsuyo-text==0.1.2', 'spacy>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'dialog-reflection',
    'version': '0.1.1',
    'description': 'A library for dialog systems that attempt to respond to messages as Reflective Listening.',
    'long_description': '# Dialog Reflection\n\nA library for dialog systems that attempt to respond to messages as Reflective Listening.\n\n## Demo\n\nNeed `git` and `poetry` to run this demo.\n\n```\n$ git clone git@github.com:sadahry/dialog-reflection.git\n$ cd dialog-reflection\n$ poetry install\n$ poetry run python examples/interactive_ja.py\n```\n\n## How to Use\n\n(WIP)\n',
    'author': 'Sadahiro YOSHIKAWA',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

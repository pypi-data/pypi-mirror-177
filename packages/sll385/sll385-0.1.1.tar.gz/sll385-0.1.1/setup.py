# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sll385']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'sll385',
    'version': '0.1.1',
    'description': 'Turn regular python lists into singly linked lists',
    'long_description': '# sll385\n\n## Description\n\nThis python package provides a function to convert a regular list into a linked list. It also provides several methods to manipulate the linked list.\n\n## Installation\n\npip install sll385\n\nhttps://pypi.org/project/sll385/',
    'author': 'Tanner Oates',
    'author_email': 'tanner.oates97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

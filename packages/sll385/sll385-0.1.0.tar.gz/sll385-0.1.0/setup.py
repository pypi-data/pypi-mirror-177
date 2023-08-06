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
    'version': '0.1.0',
    'description': 'Turn regular python lists into singly linked lists',
    'long_description': '#Test',
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

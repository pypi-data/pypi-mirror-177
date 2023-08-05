# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utbot_executor']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=6.5.0,<7.0.0']

setup_kwargs = {
    'name': 'utbot-executor',
    'version': '0.1.0',
    'description': '',
    'long_description': '# UtBot Executor\n\nUtil for python code execution and state serialization.',
    'author': 'Vyacheslav Tamarin',
    'author_email': 'vyacheslav.tamarin@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

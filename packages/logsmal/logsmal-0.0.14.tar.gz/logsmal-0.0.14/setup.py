# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logsmal', 'logsmal.independent']

package_data = \
{'': ['*']}

install_requires = \
['jsonpickle>=2.2.0,<3.0.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'logsmal',
    'version': '0.0.14',
    'description': 'Создание файлов конфигураци',
    'long_description': 'None',
    'author': 'Denis Kustov',
    'author_email': 'denis-kustov@rambler.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/denisxab/logsmal.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

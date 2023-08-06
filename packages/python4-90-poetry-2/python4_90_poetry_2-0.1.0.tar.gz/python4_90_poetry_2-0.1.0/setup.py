# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python4_90_poetry_2', 'python4_90_poetry_2.model']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1,<5.0', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'python4-90-poetry-2',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Krzysztof',
    'author_email': 'programowanie.krzysiek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

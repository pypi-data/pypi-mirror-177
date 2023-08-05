# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src\\compmec'}

packages = \
['nurbs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compmec-nurbs',
    'version': '0.2.1',
    'description': '',
    'long_description': 'None',
    'author': 'Carlos Adir',
    'author_email': 'carlos.adir@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

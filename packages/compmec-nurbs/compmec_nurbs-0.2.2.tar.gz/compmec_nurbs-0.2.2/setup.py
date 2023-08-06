# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nurbs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compmec-nurbs',
    'version': '0.2.2',
    'description': '',
    'long_description': "[![PyPi Version](https://img.shields.io/pypi/v/compmec-nurbs.svg?style=flat-square)](https://pypi.org/project/compmec-nurbs/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/compmec-nurbs.svg?style=flat-square)](https://pypi.org/project/compmec-nurbs/)\n![Tests](https://github.com/compmec/nurbs/actions/workflows/tests.yml/badge.svg)\n\n# Nurbs\n\nThis repository contains code for inteporlate functions using B-Splines and Nurbs.\n\n\n#### Features\n\n* Basic Functions\n    * Spline ```N```\n    * Rational ```R```\n    * Derivative\n* Curves\n    * Spline\n    * Rational\n* Knot operations\n    * Insertion\n    * Removal\n* Degree operations\n    * Degree elevation\n    * Degree reduction\n\n## Install\n\nThis library is available in [PyPI][pypilink]. To install it\n\n```\npip install compmec-nurbs\n```\n\nOr install it manually\n\n```\ngit clone https://github.com/compmec/nurbs\ncd nurbs\npip install -e .\n```\n\nTo verify if everything works in your machine, type the command in the main folder\n\n```\npytest\n```\n\n## Documentation\n\nIn progress\n\n\n# FAQ\n\n#### Must I learn the theory to use it?\n\nNo! Just see the examples and it will be fine\n\n#### Can I understand the code here?\n\nYes! The easier way is to look up the **python notebook** which contains the theory along examples\n\n#### Is this code efficient?\n\nNo. It's written in python and the functions were made for easy understanding, not for performance.\nThat means: It's not very fast, but it works fine.\n\n\n## Contribute\n\nPlease use the [Issues][issueslink] or refer to the email ```compmecgit@gmail.com```\n\n\n[pypilink]: https://pypi.org/project/compmec-nurbs/\n[issueslink]: https://github.com/compmec/nurbs/issues",
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

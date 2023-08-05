# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perhaps']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'perhaps',
    'version': '0.4.1',
    'description': 'Perhaps there is no data or perhaps there is',
    'long_description': "# perhaps\n\n![PyPI](https://img.shields.io/pypi/v/perhaps?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/perhaps?style=flat-square)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n> Save your time when dealing with data that *perhaps* exist.\n\n\n*Perhaps won't offer any stable APIs before v1.0.0, but I'll do my best not to break too much things*\n\n![A code screenshot showing example usage of perhaps](.github/code-snapshot.png)\n",
    'author': 'HKGx',
    'author_email': 'mail@hkgdoes.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HKGx/perhaps',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

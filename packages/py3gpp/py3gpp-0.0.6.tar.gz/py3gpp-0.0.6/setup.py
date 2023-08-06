# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3gpp']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'py3gpp',
    'version': '0.0.6',
    'description': 'functions for 5G NR signal processing',
    'long_description': '# py3gpp',
    'author': 'Benjamin Menküc',
    'author_email': 'benjamin@menkuec.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/catkira/py3gpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

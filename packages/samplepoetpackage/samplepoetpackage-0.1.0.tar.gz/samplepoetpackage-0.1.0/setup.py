# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['samplepoetpackage']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.23.3']

setup_kwargs = {
    'name': 'samplepoetpackage',
    'version': '0.1.0',
    'description': 'Testing poetry out by building a py package!',
    'long_description': 'Python poetry package ',
    'author': 'Rohan Sikand',
    'author_email': 'rsikand29@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rosikand/samplepoetpackage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

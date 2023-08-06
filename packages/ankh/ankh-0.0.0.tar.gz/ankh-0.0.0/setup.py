# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ankh']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ankh',
    'version': '0.0.0',
    'description': 'Optimized Protein Language Model',
    'long_description': 'None',
    'author': 'Ahmed Elnaggar',
    'author_email': 'amit.najjar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

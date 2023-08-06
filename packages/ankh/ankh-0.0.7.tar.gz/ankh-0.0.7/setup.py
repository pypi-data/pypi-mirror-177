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
    'version': '0.0.7',
    'description': 'Optimized Protein Language Model',
    'long_description': '<h1>Ankh</h1>\n\nAnkh: Optimized Protein Language Model\n',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lampa']

package_data = \
{'': ['*']}

install_requires = \
['bokeh==2.4.3',
 'dataclasses-json>=0.5.7,<0.6.0',
 'jupyter>=1.0.0,<2.0.0',
 'jupyterlab>=3.5.0,<4.0.0',
 'notebook>=6.5.2,<7.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pyexcel>=0.7.0,<0.8.0',
 'pystrata>=0.5.0,<0.6.0',
 'seaborn>=0.12.1,<0.13.0',
 'streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'lampa',
    'version': '0.1.4',
    'description': '',
    'long_description': '',
    'author': 'panagop',
    'author_email': 'gpanagop@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.10.8',
}


setup(**setup_kwargs)

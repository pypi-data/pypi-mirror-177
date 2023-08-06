# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ccolors']
install_requires = \
['colorama>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'ccolors',
    'version': '1.0.0',
    'description': 'Python Library for changing terminal colors!',
    'long_description': '```python\nfrom ccolors import *\n\nprint(R+"Hello World")\nprint(R+BW+"Hello Developer!")\n```',
    'author': 'ozodbeksobirjonovich',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

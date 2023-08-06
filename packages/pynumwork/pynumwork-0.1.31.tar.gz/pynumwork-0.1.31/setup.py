# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pynumwork']
setup_kwargs = {
    'name': 'pynumwork',
    'version': '0.1.31',
    'description': 'Dedicated to Ksenia @milkpink_2 :)',
    'long_description': "PyNumWork - Python module    \nCreated for simple math operations    \nIt's a test module just for fun     \nContains:     \n-Information weight container     \n-Geometrical square&perimeter/angles     \n-Number work     \nCOMMAND TO IMPORT THE MODULE:    \nfrom pynumwork import *    \nPIP COMMAND:\npip install pynumwork    \nEnjoy! :)     \n--SPACECULTENGINEER",
    'author': 'spacecultengineer',
    'author_email': 'spacecultengineer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

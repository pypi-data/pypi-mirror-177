# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reversestem',
 'reversestem.dmo',
 'reversestem.dto',
 'reversestem.dto.a',
 'reversestem.dto.b',
 'reversestem.dto.c',
 'reversestem.dto.d',
 'reversestem.dto.e',
 'reversestem.dto.f',
 'reversestem.dto.g',
 'reversestem.dto.h',
 'reversestem.dto.i',
 'reversestem.dto.j',
 'reversestem.dto.k',
 'reversestem.dto.l',
 'reversestem.dto.m',
 'reversestem.dto.n',
 'reversestem.dto.o',
 'reversestem.dto.p',
 'reversestem.dto.q',
 'reversestem.dto.r',
 'reversestem.dto.s',
 'reversestem.dto.t',
 'reversestem.dto.u',
 'reversestem.dto.v',
 'reversestem.dto.w',
 'reversestem.dto.x',
 'reversestem.dto.y',
 'reversestem.dto.z',
 'reversestem.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'unicodedata2']

setup_kwargs = {
    'name': 'reversestem',
    'version': '0.1.2',
    'description': 'Unigram Lexicon for Reverse Stem Lookups',
    'long_description': '# Reverse Stemming (reversestem)\nStemming is the technique or method of reducing words with similar meaning into their “stem” or “root” form.\n\nReverse stemming takes a “stem” or “root” form and returns all the words that have this root as a basis.\n\n## Usage\n```python\nfrom reversestem import unstem\n\nunstem(\'aggreg\')\n```\n\noutputs the stems grouped by lemma\n```json\n{\n   "aggregability":[],\n   "aggregable":[],\n   "aggregant":[\n      "aggregants"\n   ],\n   "aggregate":[\n      "aggregated",\n      "aggregately",\n      "aggregateness"\n   ],\n   "aggregating":[],\n   "aggregation":[\n      "aggregational"\n   ],\n   "aggregative":[\n      "aggregatives",\n      "aggregatively",\n      "aggregativeness"\n   ],\n   "aggregativity":[],\n   "aggregator":[]\n}\n```\n\nOr a flat list can be produced like this\n```python\nunstem(\'aggreg\', flatten=True)\n```\n\nand this outputs a simple list\n```json\n[\n   "aggregativeness",\n   "aggregational",\n   "aggregability",\n   "aggregateness",\n   "aggregativity",\n   "aggregatively",\n   "aggregatives",\n   "aggregating",\n   "aggregation",\n   "aggregately",\n   "aggregative",\n   "aggregated",\n   "aggregable",\n   "aggregants",\n   "aggregator",\n   "aggregate",\n   "aggregant"\n]\n```\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/reversestem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)

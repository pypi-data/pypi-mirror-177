# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandoc_glossary_filter']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'panflute>=2.2.3,<3.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['pandoc-glossary = pandoc_glossary_filter:main']}

setup_kwargs = {
    'name': 'pandoc-glossary-filter',
    'version': '0.2.2',
    'description': 'Pandoc filter used to generate a glossary and an acronym list common to a set of documents',
    'long_description': '# pandoc_glossary_filter\n\n## Usage\n\n```md\n<!-- GLOSSARY -->\n{g:mylabel} <!-- Inserts a glossary entry with label `mylabel` -->\n{G:mylabel} <!-- Inserts a glossary entry with label `mylabel` capitalizing the first letter -->\n{gs:mylabel} <!-- Inserts a glossary entry with label `mylabel` using the plural form -->\n{Gs:mylabel} <!-- Inserts a glossary entry with label `mylabel` capitalizing the first letter and using the plural form -->\n\n<!-- ACRONYMS -->\n{a:myacro} <!-- Insert an acronym with label `myacro` -->\n```\n\n## TODO\n\n- Add support for a full glossary document containing all the defined entries\n- Actually usable documentation\n',
    'author': 'Augusto Zanellato',
    'author_email': 'augusto.zanellato@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)

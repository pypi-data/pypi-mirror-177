# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oakx_grape']

package_data = \
{'': ['*']}

install_requires = \
['bioregistry>=0.5.136,<0.6.0',
 'click>=8.1.3,<9.0.0',
 'ensmallen==0.8.28',
 'grape',
 'importlib>=1.0.4,<2.0.0',
 'oaklib>=0.1.43,<0.2.0',
 'scipy>=1.9.0,<2.0.0',
 'tox>=3.25.1,<4.0.0']

extras_require = \
{':extra == "docs"': ['sphinx[docs]>=5.3.0,<6.0.0',
                      'sphinx-autodoc-typehints[docs]>=1.19.4,<2.0.0',
                      'sphinx-click[docs]>=4.3.0,<5.0.0',
                      'myst-parser[docs]>=0.18.1,<0.19.0',
                      'furo[docs]>=2022.9.29,<2023.0.0']}

entry_points = \
{'console_scripts': ['oakx-grape = oakx_grape.cli:main'],
 'oaklib.plugins': ['grape = '
                    'oakx_grape.grape_implementation:GrapeImplementation']}

setup_kwargs = {
    'name': 'oakx-grape',
    'version': '0.1.1',
    'description': 'oakx-grape',
    'long_description': "# oakx-grape\n\n🌳 🍇 Grape wrapper for OAK 🌳 🍇\n\n**ALPHA**\n\n## Usage\nMacbook users with M1 processor need to do a few extra steps as follows:\n\n - Download [Anaconda](https://www.anaconda.com/products/distribution).\n - `conda create --name oakx-grape-env python=3.9`\n - `conda activate oakx-grape-env`\n - `pip install poetry`\n - `poetry install`\n\nThe steps below are common to everyone.\n```\npip install oakx-grape\npoetry run runoak -i grape:sqlite:obo:pato relationships --direction both shape\n```\n### Install NVM + NPM\nThese [instructions](https://dev.to/ms314006/how-to-install-npm-through-nvm-node-version-manager-5gif) help setup nvm and npm on one's system.\n\n### Install GraphViz and OboGraphViz\n- `brew install graphviz`\n- `npm install -g obographviz`\n\n## How it works\n\nThis plugin implements a grape wrapper. The wrapper in fact wraps two adapters:\n\n1. An adaptor to ensmallen/grape, for performing performance-intensive graph operations\n2. An OAK adapter for handling everything else, including lookup by labels, search, predicate filtering, etc\n\nThere are two choices of selector:\n\n1. `grape:kgobo:{go,pato,uberon,...}`\n2. `grape:OAK-SELECTOR`\n\nwith the first pattern, the grape graph is loaded from kgobo, and the oak adapter is loaded from semantic sql\n\nwith the second, you can most existing existing OAK adapters:\n\n- sqlite/semsql\n- obo\n- rdf/owl\n\nNote you CANNOT use a backend like ubegraph or bioportal that relies on API calls\n\nThe idea is we will be able to run a notebook like this:\n\nhttps://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Monarch/PhenIO-Tutorial.ipynb\n\nWith the semsim part handled by OAK\n\n## Acknowledgements\n \nThis [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [oakx-plugin-cookiecutter](https://github.com/INCATools/oakx-plugin-cookiecutter) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).",
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)

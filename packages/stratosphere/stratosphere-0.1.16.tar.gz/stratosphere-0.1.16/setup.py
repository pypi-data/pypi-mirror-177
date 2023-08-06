# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stratosphere',
 'stratosphere.store',
 'stratosphere.store.db',
 'stratosphere.utils']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'colorama>=0.4.6,<0.5.0',
 'dask[complete]>=2022.11.0,<2023.0.0',
 'ipywidgets>=8.0.2,<9.0.0',
 'joblib>=1.2.0,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'sqlalchemy-utils>=0.38.3,<0.39.0',
 'sqlalchemy>=1.4.44,<2.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.64.1,<5.0.0',
 'ulid-py>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'stratosphere',
    'version': '0.1.16',
    'description': 'A lightweight experimentation toolkit for data scientists.',
    'long_description': '# Stratosphere\n\n*A lightweight experimentation toolkit for data scientists.*\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stratosphere)\n![PyPI - License](https://img.shields.io/pypi/l/stratosphere)\n![PyPI - Version](https://img.shields.io/pypi/v/stratosphere)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/stratosphere)\n![PyPI - Installs](https://img.shields.io/pypi/dm/stratosphere)\n![Black - Code style](https://img.shields.io/badge/code%20style-black-000000.svg)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dkKBwhm4L_MMoWWtfD0FAFgTFP1BV40c)\n\nDesigned for simplicity, efficiency and robustness. `stratosphere` lets you:\n\n1. **Define** programmatically your experiments\n2. **Execute** them in parallel with different backends\n3. **Track** their real-time metrics and final results\n4. **Store** them as serialized objects and tabular data in your database(s)\n5. **Query** them with the best-suited interface: SQL, Pandas and Python\n\nBuilt on top of solid components: [SQLAlchemy](https://www.sqlalchemy.org/), [SQLite](https://www.sqlite.org/), [Pandas](https://pandas.pydata.org/), [Joblib](https://joblib.readthedocs.io/en/latest/) and [Dask](https://www.dask.org/).\n\n![Stratosphere](https://raw.githubusercontent.com/elehcimd/stratosphere/b6993093ae617b98bcabf5d1d3153a7c3e1383a5/logo.png)\n\n## Installation\n\nIt officially requires `Python >=3.8.15,<3.11`, but it can be forced to work smoothly with `Python 3.7.15`.\n\n* With PyPI: `pip install stratosphere --upgrade`\n* With Poetry: `poetry add stratosphere`\n\nTo run it on [Google Colab](https://colab.research.google.com/), install it as follows:\n\n```\n# Install dependencies/update packages\n!pip install pandas joblib sqlalchemy sqlalchemy-utils ulid-py psycopg2-binary \\\n  cloudpickle colorama tabulate ipywidgets tqdm scikit-learn "dask[complete]" --upgrade\n# Install the latest compatible stratosphere version, ignoring the python version and dependencies\n!pip install stratosphere==0.1.13 --ignore-requires-python --no-dependencies\n```\n\n## Documentation\n\n* Try it now! [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dkKBwhm4L_MMoWWtfD0FAFgTFP1BV40c)\n* Follow the [tutorial notebooks](./notebooks/) to learn the basic concepts. You can run the tutorial notebooks in Colab as follows:\n\n  1. Open the notebook on Github, and substitute `github.com` with `githubtocolab.com` in the URLs\n  2. Add a cell at the beginning, installing `stratosphere` following the Installation instructions for Colab\n\n\n## Project pages\n\n* [PyPI](https://pypi.org/project/stratosphere/)\n* [Github](https://github.com/elehcimd/stratosphere)\n\n## License\n\nThis project is licensed under the terms of the [BSD 3-Clause License](https://github.com/elehcimd/stratosphere/blob/main/LICENSE).\n\n## Development\n\nSee the [development](https://github.com/elehcimd/stratosphere/blob/main/DEVELOPMENT.md) page.\n\n## Contributing\n\nWork in progress!\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elehcimd/stratosphere',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.15,<3.11',
}


setup(**setup_kwargs)

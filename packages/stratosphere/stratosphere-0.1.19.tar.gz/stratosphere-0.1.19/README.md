# Stratosphere

*A lightweight experimentation toolkit for data scientists.*

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stratosphere)
![PyPI - License](https://img.shields.io/pypi/l/stratosphere)
![PyPI - Version](https://img.shields.io/pypi/v/stratosphere)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/stratosphere)
![PyPI - Installs](https://img.shields.io/pypi/dm/stratosphere)
![Black - Code style](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dkKBwhm4L_MMoWWtfD0FAFgTFP1BV40c)
[![Open in Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/elehcimd/stratosphere/HEAD)

Designed for simplicity, efficiency and robustness. `stratosphere` lets you:

1. **Define** programmatically your experiments
2. **Execute** them in parallel with different backends
3. **Track** their real-time metrics and final results
4. **Store** them as serialized objects and tabular data in your database(s)
5. **Query** them with the best-suited interface: SQL, Pandas and Python

Built on top of solid components: [SQLAlchemy](https://www.sqlalchemy.org/), [SQLite](https://www.sqlite.org/), [Pandas](https://pandas.pydata.org/), [Joblib](https://joblib.readthedocs.io/en/latest/) and [Dask](https://www.dask.org/).

![Stratosphere](https://raw.githubusercontent.com/elehcimd/stratosphere/b6993093ae617b98bcabf5d1d3153a7c3e1383a5/logo.png)

## Installation

It officially requires `Python >= 3.8.0`, but it can be forced to work smoothly also on `Python 3.7.13-15` (supporting Colab, Binder).

On `Python >= 3.8.0`:

* With PyPI: `pip install stratosphere --upgrade`
* With Poetry: `poetry add stratosphere@latest`

On `Python 3.7.13-15` with [Google Colab](https://colab.research.google.com/) or 
[Binder](https://mybinder.org), execute the following in a cell:

```
# Install dependencies
!pip install pandas joblib sqlalchemy sqlalchemy-utils ulid-py cloudpickle colorama tqdm --upgrade

# Install extras, required to run the tutorial
!pip install tabulate scikit-learn dask[complete] --upgrade
```

## Documentation

Follow the [tutorial notebooks](./notebooks/) to learn the basic concepts.
You can run the notebooks locally, on Colab and on Binder.

## Project pages

* [PyPI](https://pypi.org/project/stratosphere/)
* [Github](https://github.com/elehcimd/stratosphere)

## License

This project is licensed under the terms of the [BSD 3-Clause License](https://github.com/elehcimd/stratosphere/blob/main/LICENSE).

## Development

See the [development](https://github.com/elehcimd/stratosphere/blob/main/DEVELOPMENT.md) page.

## Contributing

Work in progress!

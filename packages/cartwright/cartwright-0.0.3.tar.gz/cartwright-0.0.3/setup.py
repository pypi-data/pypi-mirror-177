# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cartwright',
 'cartwright.analysis',
 'cartwright.categories',
 'cartwright.datasets',
 'cartwright.models',
 'cartwright.resources']

package_data = \
{'': ['*']}

install_requires = \
['arrow==1.0.3',
 'faker>=14.0',
 'fuzzywuzzy==0.18.0',
 'joblib==1.0.1',
 'numpy>=1.19',
 'pandas>=1.1',
 'pydantic==1.8.2',
 'python-levenshtein==0.20.7',
 'scipy>=1.5',
 'torch>=1.8',
 'torchvision>=0.9']

entry_points = \
{'console_scripts': ['cartwright = cartwright.categorize:main']}

setup_kwargs = {
    'name': 'cartwright',
    'version': '0.0.3',
    'description': 'A recurrent neural network paired with heuristic methods that automatically infer geospatial, temporal and feature columns',
    'long_description': '\n# Cartwright\n![Tests](https://github.com/jataware/cartwright/actions/workflows/tests.yml/badge.svg)\n\n<img src="docs/assets/cartwright-logo.png" width="175px" align="left"/>\nCartwright is a data profiler that identifies and categorizes spatial and temporal features. Cartwright uses deep learning, natural language processing, and a variety of heuristics to determine whether a column in a dataset contains spatial or temporal information and, if so, what is specifically contained.\n\nCartwright was built to automate complex data pipelines for heterogenous climate and geopolitical data that are generally oriented around geospatial and temporal features (_think maps and time series_). The challenge that Cartwright solves is automatically detecting those features so they can be parsed and normalized. This problem turns out to be quite tricky, but Cartwright makes it simple.\n\nCartwright can easily detect things like `country`, `day`, `latitude`, and many other location and time types. Check out Cartwright\'s [supported categories](https://jataware.github.io/cartwright/categories.html) for a complete listing!\n\nCartwright is easy to install and works with pretty much any tabular data. It\'s easy to add new categories too! Learn more about the methodology behind Cartwright, its API, and how to contribute in our [docs](https://jataware.github.io/cartwright).\n\n## Installation\n\nYou can install Cartwright from PyPi with `pip install cartwright`.\n\n## Using Cartwright\n\nImagine we have the following weather dataset:\n\n| x_value  |  y_value   | recorded_at | rainfall |\n|:---------|:----------:|------------:|--------|\n| 7.942658 | 107.240322 | 07/14/1992  | .2     |\n| 7.943745 | 137.240633 | 07/15/1992  | .1     |\n| 7.943725 | 139.240664 | 07/16/1992  | .3     |\n\n\nTo the human observer, it\'s pretty obvious that `x_value` is the longitude column, `y_value` the latitude, `recorded_at` the date, and `rainfall` the actual weather measurement. However, if we\'re trying to automatically ingest this data into a weather model, we would benefit from knowing this _without human observation_. Enter Cartwright:\n\n```    \nfrom pprint import pprint\nfrom cartwright import categorize\n\ncartwright = categorize.CartwrightClassify()\ncategories = cartwright.categorize(path="path/to/data.csv")\n\npprint(categories, sort_dicts=False)\n```    \n\nWe\'ve now categoriezed each column in this dataset and have automatically determined which column represents latitude, longitude and date. We\'ve also learned the time format (`%m/%d/%Y`) of the date feature.\n\n```\n{\'x_value\': {\'category\': <Category.geo: \'geo\'>,\n             \'subcategory\': <Subcategory.longitude: \'longitude\'>,\n             \'format\': None},\n \'y_value\': {\'category\': <Category.geo: \'geo\'>,\n             \'subcategory\': <Subcategory.latitude: \'latitude\'>,\n             \'format\': None},\n \'recorded_at\': {\'category\': <Category.time: \'time\'>,\n                \'subcategory\': <Subcategory.date: \'date\'>,\n                \'format\': \'%m/%d/%Y\'}}\n```\n\nWith this information we can now convert the date values to a timestamp and plot a timeseries with other features.\n\n## Resolution Detection\n\nIn addition to its ability to categorize spatial and temporal features, Cartwright can determine their resolution. For example, given a dataset like:\n\n```\ndate,temperature(C)\n2019-01-01 00:00:00, 10.2\n2019-01-01 02:00:00, 11.7\n2019-01-01 04:00:00, 12.3\n...\n2019-12-31 22:00:00, 10.1\n```\n\nCartwright can detect it\'s temporal resolution:\n\n```\nResolution(\n    uniformity=Uniformity.PERFECT,\n    unit=TimeUnit.HOUR,\n    resolution=2.0,\n    error=0.0,\n)\n```\n\nFor gridded data, which is common in the scientific domain, Cartwright can also determine the spatial resolution (grid size). Check out the docs to learn more about using Cartwright to detect [temporal resolution](https://jataware.github.io/cartwright/temporal_resolution.html) and [spatial resolution](https://jataware.github.io/cartwright/geospatial_resolution.html).',
    'author': 'Kyle Marsh',
    'author_email': 'kyle@jataware.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

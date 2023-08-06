# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfds_ds_toolbox',
 'dfds_ds_toolbox.analysis',
 'dfds_ds_toolbox.feature_extraction',
 'dfds_ds_toolbox.feature_selection',
 'dfds_ds_toolbox.logging',
 'dfds_ds_toolbox.model_selection',
 'dfds_ds_toolbox.profiling']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4,<4.0',
 'pandas>=1.0,<2.0',
 'rich>=12.0,<13.0',
 'scikit-learn>=1.0,<2.0',
 'scipy>1.7.2',
 'statsmodels>=0.13,<0.14']

setup_kwargs = {
    'name': 'dfds-ds-toolbox',
    'version': '0.10.2',
    'description': 'A toolbox for data science',
    'long_description': '# Introduction\n\nThis repo is intended to contain a packaged toolbox of some neat,\nfrequently-used data science code snippets and functions. The intention is that\nthe classes should be compatible with the\n[sklearn](https://scikit-learn.org/stable/) library.\n\nHave a look at https://dfds-ds-toolbox.readthedocs.io for user guide.\n\nAlready implemented:\n\n- Model selector for regression and classification problems\n- Profiling tool for generating stats files of the execution time of a function\n\nTo be implemented in the future:\n\n- Preprocessing\n\n  - Imbalanced datasets\n  - Outlier detection & handling\n  - Missing value imputation\n\n- Feature generation\n\n  - Binning\n  - Type variables, create multiple features\n  - Timestamp, seasonality variables\n  - Object: onehot, grouping, etc.\n\n- Performance analysis (plots, summary, error analysis)\n\nMore ideas might arise in the future and should be added to the list.\n\nA guide on how to install the package and some working examples of how to use\nthe classes can be found in later sections.\n\n# Getting Started\n\n## Install locally\n\nWe use poetry as the package manager and build tool. Make sure you have poetry\ninstalled locally, then run\n\n```shell\npoetry install\n```\n\nRun tests to see everything working\n\n```shell\npoetry run pytest\n```\n\n## Install this library in another repo\n\nMake sure your virtual environment is activated, then install the required\npackages\n\n```shell\npython -m pip install --upgrade pip\n```\n\nIf you want to install the package `dfds_ds_toolbox` version 0.8.0, you should\nrun\n\n```shell\npip install dfds_ds_toolbox==0.8.0\n```\n\n# Versions\n\nSee changelog at\n[GitHub](https://github.com/dfds-data/dfds-ds-toolbox/releases).\n\n# Contribute\n\nWe want this library to be useful across many data science projects. If you have\nsome standard utilities that you keep using in your projects, please add them\nhere and make a PR.\n\n## Releasing a new version\n\nWhen you want to release a new version of this library to\n[PyPI](https://pypi.org/project/dfds-ds-toolbox/), there is a few steps you must\nfollow.\n\n1. Update the version in `setup.py`. We follow\n   [Semantic Versioning](https://semver.org/), so think about if there is any\n   breaking changes in your release when you increment the version.\n2. Draft a new release in\n   [Github](https://github.com/dfds-data/dfds-ds-toolbox/releases/new). You can\n   follow this link or click the "Draft a new release button" on the "releases"\n   page.\n   1. Here you must add a tag in the form "v<VERSION>", for example "v0.9.2".\n      The title should be the same as the tag.\n   2. Add release notes. The easiest is to use the button "Auto-generate release\n      notes". That will pull titles of completed pull requests. Modify as\n      needed.\n3. Click "Publish release". That will start a\n   [Github Action](https://github.com/dfds-data/dfds-ds-toolbox/actions) that\n   will build the package and upload to PyPI. It will also build the\n   documentation website.\n\n## Documentation\n\n### Website\n\nThe full documentation of this package is available at\nhttps://dfds-ds-toolbox.readthedocs.io\n\nTo build the documentation locally run:\n\n```shell\npip install -r docs/requirements.txt\ncd docs/\nsphinx-apidoc -o . ../dfds_ds_toolbox/ ../*tests*\nmake html\n```\n\nNow, you can open the documentation site in `docs/_build/index.html`.\n\n### Style\n\nWe are using Googles\n[Python style guide](https://google.github.io/styleguide/pyguide.html#381-docstrings)\nconvention for docstrings. This allows us to make an up-to-date documentation\nwebsite for the package.\n\nIn short, every function should have a short one-line description, optionally a\nlonger description afterwards and a list of parameters. For example\n\n```python\ndef example_function(some_parameter: str, optional_param: int=None) -> bool:\n    """This function does something super smart.\n\n    Here I will dive into more detail about the smart things.\n    I can use several lines for that.\n\n    Args:\n        some_parameter: Name of whatever\n        optional_param: Number of widgets or something. Only included when all the starts align.\n\n    Returns:\n         An indicator describing if something is true.\n    """\n```\n\nThere are many other style issues that we can run into, but if you follow the\nGoogle style guide, you will probably be fine.\n\n### Examples\n\nTo show the intended use and outcome of some of the included methods, we have\nincluded a gallery of plots in `examples/`. To make a new example create a new\nfile and name it something like `plot_<whatever>.py`. Start this file with a\ndocstring, for example\n\n```python\n"""\nUnivariate plots\n================\n\nFor a list of features separate in bins and analysis the target distribution in both Train and Test\n"""\n```\n\nand after this add the python code needed to create the example plot.\n',
    'author': 'Data Science Chapter at DFDS',
    'author_email': 'urcha@dfds.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dfds-ds-toolbox.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

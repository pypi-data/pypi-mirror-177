# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convexgating']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1',
 'anndata>=0.7.2',
 'click>=8.0.0',
 'matplotlib>=3.5.0',
 'numba>=0.11.0',
 'numpy==1.19.5',
 'pandas>=1.3.0',
 'pydot>=1.4.1',
 'python-igraph>=0.9.11',
 'rich>=10.3.0',
 'scanpy>=1.5',
 'scikit-learn>=1.1.1',
 'scikit-misc>=0.1.3',
 'scipy>=1.6.0',
 'seaborn>=0.10.0',
 'tk>=0.1.0',
 'torch==1.7.1',
 'tqdm>=4.62.0',
 'umap-learn>=0.5.1']

entry_points = \
{'console_scripts': ['convexgating = convexgating.__main__:main']}

setup_kwargs = {
    'name': 'convexgating',
    'version': '0.1.0',
    'description': 'ConvexGating is a Python tool to infer optimal gating strategies for flow cytometry and cyTOF data.',
    'long_description': 'convexgating\n===========================\n\n|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/convexgating.svg\n   :target: https://pypi.org/project/convexgating/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/convexgating\n   :target: https://pypi.org/project/convexgating\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/buettnerlab/convexgating\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/convexgating/latest.svg?label=Read%20the%20Docs\n   :target: https://convexgating.readthedocs.io/\n   :alt: Read the documentation at https://convexgating.readthedocs.io/\n.. |Build| image:: https://github.com/buettnerlab/convexgating/workflows/Build%20convexgating%20Package/badge.svg\n   :target: https://github.com/buettnerlab/convexgating/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/buettnerlab/convexgating/workflows/Run%20convexgating%20Tests/badge.svg\n   :target: https://github.com/buettnerlab/convexgating/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/buettnerlab/convexgating/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/buettnerlab/convexgating\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\nConvex gating is a Python package to infer an optimal gating strategy from flow, cyTOF or Ab/CITE-seq data. Convex gating expects a labelled input (for instance, from clustering) and returns a gating panel to separate the selected group of events (e.g. a cluster) from all other events (see Fig. 1a).\nFor each cluster, it reports the purity (precision), yield (recall) and the harmonic mean of both metrics (F1 score) for each gate hierarchy and the entire gating strategy. It relies on the scanpy/anndata for the data format and data pre-processing and further on PyTorch for stochastic gradient descent. Therefore, resulting gates may slightly vary.\n\n.. image:: https://github.com/buettnerlab/convexgating/blob/main/figures/fig1_v4.PNG\n   :width: 800\n   :alt: overview\n\nThe iterative procedure to find a suitable gate before applying the convex hull is illustrated in the following graphic.\n\n\n.. image:: https://github.com/buettnerlab/convexgating/blob/main/figures/fig_update_step_v5.png\n   :width: 800\n   :alt: Update\n\n\nInstallation\n------------\n\nYou can install *convexgating* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install convexgating\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\n\nCredits\n-------\n\nThis package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\n\n.. _cookietemple: https://cookietemple.com\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Usage: https://convexgating.readthedocs.io/en/latest/usage.html\n',
    'author': 'Vincent Friedrich',
    'author_email': 'vf2101@online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/buettnerlab/convexgating',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)

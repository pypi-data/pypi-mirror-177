# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reconcile']

package_data = \
{'': ['*']}

install_requires = \
['blackjax>=0.9.6,<0.10.0',
 'chex>=0.1.5,<0.2.0',
 'flax>=0.6.1,<0.7.0',
 'numpy>=1.23.4,<2.0.0',
 'optax>=0.1.3,<0.2.0',
 'pandas>=1.5.1,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'probabilistic-reconciliation',
    'version': '0.0.1',
    'description': 'Probabilistic reconciliation of time series forecasts',
    'long_description': '# reconcile\n\n[![status](http://www.repostatus.org/badges/latest/concept.svg)](http://www.repostatus.org/#concept)\n[![ci](https://github.com/dirmeier/reconcile/actions/workflows/ci.yaml/badge.svg)](https://github.com/dirmeier/reconcile/actions/workflows/ci.yaml)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f0a254348e894c7c85b4e979bc81f1d9)](https://www.codacy.com/gh/dirmeier/reconcile/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dirmeier/reconcile&amp;utm_campaign=Badge_Grade)\n\n> Probabilistic reconciliation of time series forecasts\n\n## About\n\nReconcile implements probabilistic time series forecast reconciliation methods introduced in\n\n1) Zambon, Lorenzo, Dario Azzimonti, and Giorgio Corani. "Probabilistic reconciliation of forecasts via importance sampling." arXiv preprint arXiv:2210.02286 (2022).\n2) Panagiotelis, Anastasios, et al. "Probabilistic forecast reconciliation: Properties, evaluation and score optimisation." European Journal of Operational Research (2022).\n\nThe package implements\n\n- methods to compute summing/aggregation matrices for grouped and hierarchical time series,\n- an abstract base forecasting class,\n- reconciliation methods for forecasts based on sampling and optimization\n\nAn example application can be found in `examples/reconciliation.py`\n\n## Installation\n\n\nTo install from PyPI, call:\n\n```bash\npip install reconile\n```\n\nTo install the latest GitHub <RELEASE>, just call the following on the\ncommand line:\n\n```bash\npip install git+https://github.com/dirmeier/reconcile@<RELEASE>\n```\n\n## Author\n\nSimon Dirmeier <a href="mailto:sfyrbnd @ pm me">sfyrbnd @ pm me</a>\n',
    'author': 'Simon Dirmeier',
    'author_email': 'sfyrbnd@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)

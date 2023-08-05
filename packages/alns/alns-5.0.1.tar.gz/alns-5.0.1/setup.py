# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alns',
 'alns.accept',
 'alns.accept.tests',
 'alns.select',
 'alns.select.tests',
 'alns.stop',
 'alns.stop.tests',
 'alns.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=2.2.0', 'numpy>=1.15.2']

setup_kwargs = {
    'name': 'alns',
    'version': '5.0.1',
    'description': 'A flexible implementation of the adaptive large neighbourhood search (ALNS) algorithm.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/alns.svg)](https://badge.fury.io/py/alns)\n[![ALNS](https://github.com/N-Wouda/ALNS/actions/workflows/alns.yaml/badge.svg)](https://github.com/N-Wouda/ALNS/actions/workflows/alns.yaml)\n[![Documentation Status](https://readthedocs.org/projects/alns/badge/?version=latest)](https://alns.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/N-Wouda/ALNS/branch/master/graph/badge.svg)](https://codecov.io/gh/N-Wouda/ALNS)\n\nThis package offers a general, well-documented and tested\nimplementation of the adaptive large neighbourhood search (ALNS)\nmeta-heuristic, based on the description given in [Pisinger and Ropke\n(2010)][1]. It may be installed in the usual way as\n```\npip install alns\n```\n\n### Examples\nIf you wish to dive right in, the [documentation][7] contains example notebooks\nshowing how the ALNS library may be used. These include:\n\n- The travelling salesman problem (TSP), [here][2]. We solve an instance of 131\n  cities in one minute to a 2% optimality gap, using very simple destroy and\n  repair heuristics.\n- The capacitated vehicle routing problem (CVRP), [here][8]. We solve an \n  instance with 241 customers to within 3% of optimality using a combination\n  of a greedy repair operator, and a _slack-induced substring removal_ destroy\n  operator.\n- The cutting-stock problem (CSP), [here][4]. We solve an instance with\n  180 beams over 165 distinct sizes to within 1.35% of optimality in\n  only a very limited number of iterations.\n- The resource-constrained project scheduling problem (RCPSP), [here][6]. We solve \n  an instance with 90 jobs and 4 resources to within 4% of the best known solution,\n  using a number of different operators and enhancement techniques from the \n  literature.\n- The permutation flow shop problem (PFSP), [here][9]. We solve an instance with\n  50 jobs and 20 machines to within 1.5% of the best known solution. Moreover,\n  we demonstrate multiple advanced features of ALNS, including auto-fitting the\n  acceptance criterion and adding local search to repair operators. We also\n  demonstrate how one could tune ALNS parameters.\n\nFinally, the features notebook gives an overview of various options available \nin the `alns` package. In the notebook we use these different options to solve\na toy 0/1-knapsack problem. The notebook is a good starting point for when you\nwant to use different schemes, acceptance or stopping criteria yourself. It is\navailable [here][5].\n\n## How to use\nOur [documentation][7] provides a complete overview of the `alns` package. In \nshort: the `alns` package exposes two classes, `ALNS` and `State`. The first\nmay be used to run the ALNS algorithm, the second may be subclassed to\nstore a solution state - all it requires is to define an `objective`\nmember function, returning an objective value.\n\nThe ALNS algorithm must be supplied with an _operator selection scheme_, an\n_acceptance criterion_, and a _stopping criterion_. These are explained further\nin the documentation.\n\n## References\n- Pisinger, D., and Ropke, S. (2010). Large Neighborhood Search. In M.\n  Gendreau (Ed.), _Handbook of Metaheuristics_ (2 ed., pp. 399-420).\n  Springer.\n- Santini, A., Ropke, S. & Hvattum, L.M. (2018). A comparison of\n  acceptance criteria for the adaptive large neighbourhood search\n  metaheuristic. *Journal of Heuristics* 24 (5): 783-815.\n\n[1]: http://orbit.dtu.dk/en/publications/large-neighborhood-search(61a1b7ca-4bf7-4355-96ba-03fcdf021f8f).html\n[2]: https://alns.readthedocs.io/en/latest/examples/travelling_salesman_problem.html\n[3]: https://link.springer.com/article/10.1007%2Fs10732-018-9377-x\n[4]: https://alns.readthedocs.io/en/latest/examples/cutting_stock_problem.html\n[5]: https://alns.readthedocs.io/en/latest/examples/alns_features.html\n[6]: https://alns.readthedocs.io/en/latest/examples/resource_constrained_project_scheduling_problem.html\n[7]: https://alns.readthedocs.io/en/latest/\n[8]: https://alns.readthedocs.io/en/latest/examples/capacitated_vehicle_routing_problem.html\n[9]: https://alns.readthedocs.io/en/latest/examples/permutation_flow_shop_problem.html\n',
    'author': 'Niels Wouda',
    'author_email': 'n.wouda@apium.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/N-Wouda/ALNS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

.. |python| image:: https://img.shields.io/badge/python-3.9-blue.svg
   :alt: python 3.9

.. |license| image:: https://img.shields.io/pypi/l/cify
   :alt: license pypi
   :target: https://opensource.org/licenses/MIT

.. |logo| image:: data/cify-main-logo-slogan.png
  :target: https://davidmccleave.github.io/cify/
  :alt: CIFY

.. _Documentation: https://davidmccleave.github.io/cify/

|python| |license|

|logo|

Documentation_ / Installation_ / Usage_ / Contributing_ / Contact_

CIFY: Computational Intelligence Framework for pYthon
=============================================================================

.. note::
    We are currently rewriting CIFY to improve performance and solidify the implementations of ideas 
    explored whilst writing this project. The new version can be found 
    `here (Kyle Erwin's fork) <https://github.com/KyleErwin/cify/>`_. 
    It is important to note that the new version is in its infancy and does not contain most of 
    the functionality shown by this version. We believe rewriting the framework with more time and pairs
    of eyes will result in a better foundation for more advanced concepts to be incorporated.

CIFY is a framework for computational intelligence algorithms written in
Python. The goal of the project is to create a framework that allows users to
easily and reliably implement nature-inspired metaheuristics. The framework
provides a set of very simple abstractions for implementing metaheuristics,
objective functions, running experiments and collecting results.

The guiding principles of the project are: 

- **Low barrier of entry**. Reading the tutorial or looking at the examples is
  all you should need to start working with CIFY.
- **Reproducibility**. Experiments with stochastic operations should be easily
  reproducible.
- **Speed**. Computational time should be kept to a minimum.
- **Tests and documentation**. All code should be thoroughly tested and
  documented.

Quickstart
********************************************************************************

.. warning::
    When installing CIFY from pip you will be installing the fork found 
    `here (Kyle Erwin's fork) <https://github.com/KyleErwin/cify/>`_. 

```bash
pip install cify
```

or clone the repo and install CIFY to your environment using

```bash
cd CIFY
pip install -e .
```

Basic PSO Example
********************************************************************************

Use the following example to get started or refer to the documentation for more
details.

.. code-block:: python

   import cify as ci
   from cify.si.pso.algorithm import InertiaWeightPSO

   # Set internal seed
   ci.set_seed(0)

   # 1. Define objective function.
   obj_func = ci.get_objective_function('rosenbrock', ci.Optimization.Min)

   # 2. Create swarm and metaheuristic.
   swarm = ci.get_swarm(50, obj_func=obj_func)
   pso = InertiaWeightPSO(obj_func, swarms=[swarm])

   # 3. Perform 100 iterations and return the statistics of the last 5.
   pso.execute(100)
   pso.statistics.tail(5)

.. _Contributing:

Contributing
********************************************************************************

If you wish to contribute to CIFY, you'll need to clone the repository and install the necessary
dependencies first. The steps are outlined in a tutorial on the Documentation_ website.

Useful Information
~~~~~~~~~~~~~~~~~~

`docs/` contains the Sphinx website files.

`cify/` contains the CIFY source code.

To generate an interactive coverage report, first cd into the root directory, then run the commands
below:

.. code-block:: bash

    coverage run -m pytest
    coverage html --omit="*/test*" --precision=2 && open htmlcov/index.html

These commands will run pytest to generate the coverage report, then convert the generated SQL database into
HTML and open the web page in your default browser.

.. _Contact:

Contact
********************************************************************************

For any questions, contact me at my LinkedIn:

| `David McCleave <https://www.linkedin.com/in/david-mccleave-326106243/>`_
| Stellenbosch University

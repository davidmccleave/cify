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

.. TODO:
.. Each code repository must contain a README file with instructions on 
.. (i) how to start up the environment, including automatic resolution of any dependencies, 
.. (ii) how to run the application, and 
.. (iii) how to run experiments or tests.

NOTE: We are currently rewriting CIFY to improve performance and solidify ideas that were
rushed in the past. This new version can be found here `here (Kyle Erwin's fork) 
<https://github.com/KyleErwin/cify/>`_.

The official repository for the Python CI framework, formerly known as CIFY.
This open-source framework provides easy access to static methods and classes that
simplify the process of nature-inspired optimization in Python. For more information,
consult the Documentation_.

.. _Installation:

Installation
********************************************************************************

First, it is necessary to make sure you have a working Python 3 environment installed.

To install the latest stable release via `pip`:

.. code-block:: bash

    pip install cify


.. _Usage:

Basic PSO Example
********************************************************************************

Below is a simple example that first sets a global seed for all stochastic operations,
then defines an objective function to optimize, optimizes this function using a PSO
algorithm, and finally, outputs the results of the last five iterations.

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

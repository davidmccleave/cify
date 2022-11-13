.. |python| image:: https://img.shields.io/badge/python-3.9-blue.svg
   :alt: python 3.9

.. |license| image:: https://img.shields.io/pypi/l/cify
   :alt: license pypi
   :target: https://opensource.org/licenses/MIT

.. |logo| image:: data/cify-main-logo-slogan.png
  :target: https://computer-science.pages.cs.sun.ac.za/rw771/2022/22628274-AE3-src/
  :alt: CIFY

.. _Documentation: https://computer-science.pages.cs.sun.ac.za/rw771/2022/22628274-AE3-src/

|python| |license|

|logo|

Documentation_ / Useful_ / Installation_ / Usage_ / Contact_

CIFY: Computational Intelligence Framework for pYthon
=============================================================================

.. TODO:
.. Each code repository must contain a README file with instructions on 
.. (i) how to start up the environment, including automatic resolution of any dependencies, 
.. (ii) how to run the application, and 
.. (iii) how to run experiments or tests.

The official repository for the Python CI framework, formerly known as CIFY.
This open-source framework provides easy access to static methods and classes that
simplify the process of nature-inspired optimization in Python. For more information,
consult the Documentation_.

.. _Useful:

Useful Information
********************************************************************************

`docs/` contains the Sphinx website files.

`cify/` contains the CIFY source code.

To generate an interactive coverage report, first cd into the root directory, then run the commands
below:

.. code-block:: bash

    coverage run -m pytest
    coverage html --omit="*/test*" --precision=2 && open htmlcov/index.html

These commands will run pytest to generate the coverage report, then convert the generated SQL database into
HTML and open the web page in your default browser.

.. _Installation:

Installation
********************************************************************************

First, it is necessary to make sure you have a working Python 3 environment installed.

To install the latest stable release via `pip`:

.. code-block:: bash

    pip install cify

From source:

.. code-block:: bash

    <todo: add source installation instructions here>

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
   set_seed(0)

   # Define objective function.
   obj_func = ci.get_objective_function('rosenbrock', ci.Optimization.Min)

   # Create swarm and algorithm.
   swarm = ci.get_swarm(10, obj_func=obj_func)
   pso = InertiaWeightPSO(obj_func, swarms=[swarm])

   # Perform 100 iterations and return the statistics of the last 5.
   pso.execute(100)
   pso.statistics.tail(5)


.. _Contact:

Contact
********************************************************************************

For any questions, contact me at my LinkedIn:

| `David McCleave <https://www.linkedin.com/in/david-mccleave-326106243/>`_
| Stellenbosch University

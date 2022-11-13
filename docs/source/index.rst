.. cify documentation master file, created by
   sphinx-quickstart on Sat Jul  9 13:02:39 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: images/cify-main-logo-slogan.png
   :width: 1000
   :alt: CIFY
   :align: center

Documentation
=====================

CIFY is a framework for common computational intelligence
paradigms written in Python. The goal of the framework is to
provide end users with the ability to easily and reliably
implement nature-inspired metaheuristics.
A collection of well-known metaheuristics are provided alongside tools to manipulate these metaheuristics, define
objective functions for them to optimize, and create pipelines out of collections of approaches. The framework
is built on Numpy and Pandas. Use your preferred PyData packages with seamless integration.

For more details, check out :doc:`what-is-cify`. If you want to get familiar with the framework fast, read through the
:doc:`necessary-knowledge` page.

Installation
------------

The framework is hosted on ``pip`` and can be installed directly as follows::

   pip install cify

The latest version of CIFY currently available is version 0.9.2.

Basic Example
-------------
::

   import cify as ci
   from cify.si.pso.algorithm import InertiaWeightPSO

   # 1. Set internal seed for stochastic operations.
   set_seed(0)

   # 2. Call or define an objective function.
   obj_func = ci.get_objective_function('rosenbrock', ci.Optimization.Min)

   # 3. Create swarm and algorithm.
   pso = InertiaWeightPSO(obj_func, swarms=[ci.get_swarm(10, obj_func=obj_func)])

   # 4. Execute
   pso.execute(n_iterations=100)

   # Examine results
   pso.statistics.tail(5)

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   what-is-cify
   installation
   necessary-knowledge
   tutorials
   benchmark-objective-functions
   api
   license

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

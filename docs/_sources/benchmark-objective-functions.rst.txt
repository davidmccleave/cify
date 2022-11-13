Benchmark Objective Functions
=====================================

This page contains a table listing all provided benchmark functions.

.. list-table:: Provided Benchmark Objective Functions
    :widths: 20 20 30 10 5 5 10
    :header-rows: 1

    * - Name
      - Characteristics
      - Equation
      - Minimum
      - Lower Bound
      - Upper Bound
      - n-dimensions
    * - mean-dimensions
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = \frac{1}{n} \sum_{i=1}^{n} |x_i|`
      - 0
      - -100
      - 100
      - [1,n)
    * - sphere
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = \sum_{i=1}^{n} x_i^2`
      - 0
      - -5.12
      - 5.12
      - [1,n)
    * - high-conditioned-elliptic-function
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = \sum_{i=1}^{n} {(10^6)}^{\frac{i-1}{n-1}} \cdot x_i^2`
      - 0
      - -100
      - 100
      - [1,n)
    * - discus
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = 10^6 \cdot x_1^2 + \sum_{i=2}^{n} x_i^2`
      - 0
      - -100
      - 100
      - [1,n)
    * - cosine-mixture
      - Discontinuous, Non-Differentiable, Multimodal
      - :math:`f(\mathbf{x}) = -0.1 \sum_{i=1}^{n} cos(5 \pi x_i) - \sum_{i=1}^{n} x_i^2`
      - :math:`\frac{n}{10}`
      - -1
      - 1
      - [1,n)
    * - schwefel
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = 418.9829n - \sum_{i=1}^{n} x_i sin(\sqrt{|x_i|})`
      - 0
      - -500
      - 500
      - [1,n)
    * - schwefel1
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = C \cdot \sum_{i=1}^{n} {x_i}^2`
      - 0
      - -100
      - 100
      - [1,n)
    * - price1
      - Continuous, Non-Differentiable, Multimodal
      - :math:`f(\mathbf{x}) = (|x_1| - 5)^2 + (|x_2| - 5)^2`
      - 0
      - -500
      - 500
      - 2
    * - rosenbrock
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = \sum_{i=1}^{n-1} 100 \cdot (x_{i+1} - x_{i})^2 + (x_{i} - 1)^2`
      - 0
      - -2.048
      - 2.048
      - [1,n)
    * - exponential
      - Continuous, Differentiable, Multimodal
      - :math:`f(\mathbf{x}) = e^{\frac{-1}{2} \cdot \sum_{i=1}^{n} {x_i}^2}`
      - 1
      - -1
      - 1
      - [1,n)
    * - brown
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = \sum_{i=1}^{n-1} ({x_i^2}^{x_{i+1}^2 + 1}) + ({x_{i+1}^2}^{x_i^2 + 1})`
      - 0
      - -1
      - 4
      - [1,n)
    * - qing
      - Continuous, Differentiable, Multimodal
      - :math:`f(\mathbf{x}) = \sum_{i=1}^{n} {x_i^2 - i + 1}^2`
      - 0
      - -500
      - 500
      - [1,n)
    * - rastrigin
      - Continuous, Differentiable, Unimodal
      - :math:`f(\mathbf{x}) = 10 n + \sum_{i=1}^{n} (x_i^2 - 10 \cdot cos(2\pi x_i))`
      - 0
      - -5.12
      - 5.12
      - [1,n)

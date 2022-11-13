import math
from cify.core.objective_function import ObjectiveFunction
from cify.core.optimization import Optimization
from cify.core.position import Position
from cify.global_constants import get_rng

__all__ = ['get_objective_function', 'get_position_vector']


def get_objective_function(func_name: str, optimization=Optimization.Min, n_dimensions: int = 10,
                           vector_constraints: list or dict = None, **kwargs):
    """
    Returns a stored benchmark objective function by name.

    All stored benchmark objective functions are taken from
    Jamil, M. & Yang, X.-S. A Literature Survey of Benchmark Functions For Global Optimization Problems. Int.
    Journal of Mathematical Modelling and Numerical Optimisation, 2013, 4, pp. 150-194.

    :param func_name: The name of the benchmark :class:`~cify.core.objectivefunction.ObjectiveFunction`.
    :type func_name: str
    :param optimization: The optimization type.
    :type optimization: :class:`~cify.core.optimization.Optimization`
    :param n_dimensions: The number of dimensions of the :class:`~cify.core.objectivefunction.ObjectiveFunction`
                         search space. If an :class:`ObjectiveFunction` is supplied, this field is not used.
    :type n_dimensions: int, optional
    :param vector_constraints: The vector constraints to associate with the chosen :class:`ObjectiveFunction`.
    :type vector_constraints: A list or dict

    :return: The selected benchmark objective function.
    :rtype: :class:`ObjectiveFunction`
    """
    function = None
    calc_bounds = None

    if func_name == "mean-dimensions":
        def mean_dimensions(pos):
            calc_sum = 0
            for index in pos:
                calc_sum += abs(index)
            return float(calc_sum) / len(pos)

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-100, 100])

        function = mean_dimensions
        calc_bounds = bounds

    elif func_name == "sphere":
        def sphere(pos):
            return sum([float(x)**2 for x in pos])

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-5.12, 5.12])

        function = sphere
        calc_bounds = bounds

    elif func_name == "high-conditioned-elliptic-function":
        def high_cond_elliptic_function(pos):
            calc_sum = 0
            for idx, element in enumerate(pos):
                (10**6)**((idx-1)/(len(pos)-1)) * (element**2)
            return calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-100, 100])

        function = high_cond_elliptic_function
        calc_bounds = bounds

    elif func_name == "discus":
        def discus(pos):
            calc_sum = 0.
            for idx in range(1, len(pos)):
                calc_sum += float(pos[idx])
            return (10**6) * (float(pos[0])**2) + calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-100, 100])

        function = discus
        calc_bounds = bounds

    elif func_name == "cosine-mixture":
        def cosine_mixture(pos):
            calc_sum = 0.
            for element in pos:
                calc_sum += float(math.cos(5 * math.pi * element))
            return -0.1 * calc_sum - sum([x**2 for x in pos])

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-1, 1])

        function = cosine_mixture
        calc_bounds = bounds

    elif func_name == "schwefel":
        def schwefel(pos):
            d = len(pos)
            calc_sum = 0
            for index in pos:
                calc_sum += float(index) * math.sin(math.sqrt(abs(index)))

            return 418.9829 * d - calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-500, 500])

        function = schwefel
        calc_bounds = bounds

    elif func_name == "schwefel1":
        def schwefel1(pos):
            c_param = 1
            calc_sum = 0
            for idx in range(len(pos)):
                calc_sum += pos[idx] ** 2
            return calc_sum ** c_param

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-100, 100])

        function = schwefel1
        calc_bounds = bounds

    elif func_name == "price1":
        def price1(pos):
            return (abs(pos[0]) - 5)**2 + (abs(pos[1]) - 5)**2

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-500, 500])

        function = price1
        calc_bounds = bounds

    elif func_name == "rosenbrock":
        def rosenbrock(pos):
            calc_sum = 0
            for idx in range(len(pos) - 1):
                calc_sum += 100 * ((pos[idx + 1] - (pos[idx] ** 2)) ** 2) + ((pos[idx] - 1) ** 2)
            return calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-2.048, 2.048])

        function = rosenbrock
        calc_bounds = bounds

    elif func_name == "exponential":
        def exponential(pos):
            calc_sum = 0
            for idx in range(len(pos)):
                calc_sum += pos[idx] ** 2
            return -math.exp(-0.5 * calc_sum)

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-1, 1])

        function = exponential
        calc_bounds = bounds

    elif func_name == "brown":
        def brown(pos):
            calc_sum = 0
            for idx in range(len(pos) - 1):
                calc_sum += ((pos[idx] ** 2) ** ((pos[idx + 1] ** 2) + 1)) + (
                        (pos[idx + 1] ** 2) ** ((pos[idx] ** 2) + 1)
                )
            return calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-1, 4])

        function = brown
        calc_bounds = bounds

    elif func_name == "qing":
        def qing(pos):
            calc_sum = 0
            for idx in range(len(pos)):
                calc_sum += ((pos[idx] ** 2) - (idx + 1)) ** 2
            return calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-500, 500])

        function = qing
        calc_bounds = bounds

    elif func_name == "rastrigin":
        def rastrigin(pos):
            A = 10
            calc_sum = 0
            for idx in range(len(pos)):
                calc_sum += (pos[idx]**2 - A * math.cos(2 * math.pi * pos[idx]))
            return A * len(pos) + calc_sum

        # calculate bounds
        bounds = []
        for i in range(n_dimensions):
            bounds.append([-5.12, 5.12])

        function = rastrigin
        calc_bounds = bounds

    else:
        print(f"The func_name you entered, {func_name}, is not an available function.")
        return ValueError(f"The func_name you entered, {func_name}, is not an available function.")

    return ObjectiveFunction(function=function,
                             optimization=optimization,
                             n_dimensions=n_dimensions,
                             bounds=calc_bounds,
                             vector_constraints=vector_constraints,
                             **kwargs)


def get_position_vector(obj_func: ObjectiveFunction, as_position: bool = False,
                        n_dimensions: int = None) -> list or Position:
    """
    Returns a uniformly distributed position vector as a list or a :class:`~cify.core.position.Position` object within
    the bounds of the :class:`ObjectiveFunction` search space.

    :param obj_func: The :class:`~cify.core.objectivefunction.ObjectiveFunction` object to return a position
                      vector for.
    :type obj_func: :class:`ObjectiveFunction`
    :param as_position: If True, returns a :class:`~cify.core.position.Position` object, otherwise returns a list,
                        defaults to False.
    :type as_position: bool
    :param n_dimensions: The number of dimensions of the generated position vector.
    :type n_dimensions: int, optional

    :return: A uniformly distributed random position vector.
    :rtype: list or :class:`Position`
    """
    dims = obj_func.n_dimensions
    if n_dimensions is not None:
        dims = n_dimensions

    vals = []
    for i in range(dims):
        vals.append(
            get_rng().uniform(low=obj_func.lower_bounds()[i], high=obj_func.upper_bounds()[i])
        )
    if as_position:
        return Position(vector=vals, obj_func=obj_func)
    else:
        return vals

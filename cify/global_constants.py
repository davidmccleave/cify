import numpy as np

__seed = None
__rng = np.random.default_rng(__seed)

__all__ = ['get_rng', 'set_seed']


def get_rng():
    """
    Returns the global random number generator used for stochastic operations.

    :return: The global RNG
    :rtype: :class:`numpy.Generator`
    """
    global __rng
    return __rng


def set_seed(seed):
    """
    Sets the global seed for the internal random number generator.

    :param seed: The seed value to be used by the generator, defaults to None
    :type seed: None, int, array-like[ints], numpy.SeedSequence, BitGenerator, Generator, optional
    """
    global __rng, __seed
    try:
        __seed = seed
        __rng = np.random.default_rng(__seed)
        print("CIFY: internal seed successfully set to: '%s'" % seed)
    except Exception:
        print("CIFY: internal seed could not be set!")

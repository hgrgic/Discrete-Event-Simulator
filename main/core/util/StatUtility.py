from scipy.stats import norm
from scipy.stats import gamma
import numpy as np


# center is the parameter which represents the center of the normal distribution
def get_norm_dist(_size, center=10):
    return norm.rvs(size=_size, loc=center, scale=1)


def get_gamma_dist(_size, _a):
    return gamma.rvs(a=_a, size=_size)


def get_binomial_dist(_size, probability, options=1):
    return np.random.binomial(options, probability, _size)


def get_poisson_dist(_size, _center):
    return np.random.poisson(_center, _size)

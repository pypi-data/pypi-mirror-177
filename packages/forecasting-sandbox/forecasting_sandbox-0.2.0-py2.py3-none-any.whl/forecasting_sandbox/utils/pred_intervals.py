import numpy as np 
from scipy.stats import norm


def get_zt(level = 0.95):
    x = 1 - (1 - level)/2
    return norm.ppf(x)  
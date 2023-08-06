import numpy as np

from integor import set_variable_names, Variable, get_cost_matrix, solve_ilp, get_solution


def get_is_positive(x : Variable, name : str = ''):
    """Returns the expression to add to objective function and the constraints to add to the list of constraints
    if you want to add is_positive(x) to your objective function. Experimental.
    """
    small_number = 1e-6
    big_number = 1e6
    is_positive = Variable("is_positive_" + name)
    constraint = x + big_number * is_positive >= 0      # when x is positive, is_positive can be 0 or 1. It will be 0 because its incentivized to be high. When x is negative, is_positive must be 1.
    additional_objective = small_number * is_positive   # will incentivize is_positive to be 0 (by default)
    return is_positive, constraint, additional_objective

def get_relu(): pass
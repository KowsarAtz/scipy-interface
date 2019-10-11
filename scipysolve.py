from eval_expressions import produce_scipy_input
from scipy.optimize import linprog
from constants import *

d = produce_scipy_input()

target_function_type = d[TARGET_FUNCTION_TYPE_KEY]
coefficients_inequalities = d[COEFFICIENTS_INEQUALITIES_KEY]
constants_inequalities = d[CONSTANTS_INEQUALITIES_KEY]
coefficients_equalities = d[COEFFICIENTS_EQUALITIES_KEY]
constants_equalities = d[CONSTANTS_EQUALITIES_KEY]


def solve():
    solution = {}
    res = linprog(d[TARGET_FUNCTION_COEFFICIENTS_KEY],
              A_ub=d[COEFFICIENTS_INEQUALITIES_KEY],
              b_ub=d[CONSTANTS_INEQUALITIES_KEY],
              A_eq=d[COEFFICIENTS_EQUALITIES_KEY],
              b_eq=d[CONSTANTS_EQUALITIES_KEY])
    solution[SOLUTION_KEY_SUCESS_STATUS] = res.success
    dict_ = {}
    i = -1
    for key in d[VARIABLES_KEY]:
        i += 1
        dict_[key] = res.x[i].round(ROUND_CONST)
    solution[SOLUTION_KEY_VARIABLE_VALUES] = dict_
    if d[TARGET_FUNCTION_TYPE_KEY] == MIN:
        solution[SOLUTION_KEY_MIN_VALUE] = (res.fun + d[TARGET_FUNCTION_CONSTANT_KEY]).round(ROUND_CONST)
    elif d[TARGET_FUNCTION_TYPE_KEY] == MAX:
        solution[SOLUTION_KEY_MAX_VALUE] = (-res.fun - d[TARGET_FUNCTION_CONSTANT_KEY]).round(ROUND_CONST)
    return solution
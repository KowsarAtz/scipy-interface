from constants import *

variables = []
inequality_dicts = []
equality_dicts = []
target_function_dict = {}
min_or_max_problem = None

def print_dicts():
    global inequality_dicts, equality_dicts, target_function_dict
    print("INEQUALITIES:")
    for d in inequality_dicts:
        print(d)
    print("EQUALITIES:")
    for d in equality_dicts:
        print(d)
    print("TARGET:")
    print(target_function_dict)
    
def process_dicts():
    global variables, inequality_dicts, equality_dicts, target_function_dict, min_or_max_problem
    coefficients_inequalities = []
    constants_inequalities = []
    coefficients_equalities = []
    constants_equalities = []
    target_function_coefficients = []
    target_function_constant = 0
    variables.sort()
    for ineq_dict in inequality_dicts:
        temp = []
        for key in variables:
            try:
                temp_val = ineq_dict[key]
            except KeyError:
                temp_val = 0
            temp += [temp_val]
        coefficients_inequalities += [temp]
        temp_val = None
        try:
            temp_val = ineq_dict[CONSTANT_VALUE]
        except KeyError:
            temp_val = 0
        constants_inequalities += [(-1)*temp_val]
    for eq_dict in equality_dicts:
        temp = []
        for key in variables:
            try:
                temp_val = eq_dict[key]
            except KeyError:
                temp_val = 0
            temp += [temp_val]
        coefficients_equalities += [temp]
        constants_equalities += [(-1)*eq_dict[CONSTANT_VALUE]]
    for key in variables:
        try:
            temp_val = target_function_dict[key]
        except KeyError:
            temp_val = 0
        target_function_coefficients += [temp_val]
    temp_val = 0
    try:
        temp_val = target_function_dict[CONSTANT_VALUE]
    except KeyError:
        temp_val = 0
    target_function_constant = temp_val
    f = (lambda x: None if x == [] else x)
    return {
        VARIABLES_KEY: f(variables),
        TARGET_FUNCTION_TYPE_KEY: min_or_max_problem,
        TARGET_FUNCTION_COEFFICIENTS_KEY: f(target_function_coefficients),
        TARGET_FUNCTION_CONSTANT_KEY: target_function_constant,
        COEFFICIENTS_INEQUALITIES_KEY: f(coefficients_inequalities), 
        CONSTANTS_INEQUALITIES_KEY: f(constants_inequalities),
        COEFFICIENTS_EQUALITIES_KEY: f(coefficients_equalities),
        CONSTANTS_EQUALITIES_KEY: f(constants_equalities)
    }

def add_variable(var):
    global variables
    if var not in variables:
        variables += [var]

def merge_dicts(dict1, dict2):
    dict3 = dict1.copy()
    for key in dict2.keys():
        try:
            dict3[key] += dict2[key]
        except KeyError:
            dict3[key] = dict2[key]
    return dict3

def process_expression(expression, cof, dict_):
    expression = expression.replace('-','+-1*')
    terms = expression.split('+')
    for term in terms:
        variable_count = 0
        faced_value_error = False
        factors = term.split('*')
        key = ''
        temp = 1
        tempfloat = 0.0
        for factor in factors:
            try:
                tempfloat = float(factor)
                temp *= tempfloat
            except ValueError:
                variable_count += 1
                if variable_count > 1:
                    return LINEAR_EXPRESSION_SYNTAX_ERROR
                faced_value_error = True
                key = "%s" % factor.replace(' ','')
        if faced_value_error:
            try:
                dict_[key] += temp*cof
            except KeyError:
                dict_[key] = temp*cof
                add_variable(key)
        else:
            try:
                dict_[CONSTANT_VALUE] += temp*cof
            except KeyError:
                dict_[CONSTANT_VALUE] = temp*cof
    return dict_

def process_target_function(expression, type_):
    global target_function_dict
    factor = type_
    dict_ = process_expression(expression, factor, {})
    target_function_dict = dict_

def process_inequality(expressions, type_):
    global inequality_dicts
    left_side_factor = type_
    right_side_factor = -1 * type_
    result_dict = merge_dicts(
        dict1=process_expression(expressions[0], left_side_factor, {}),
        dict2=process_expression(expressions[1], right_side_factor, {}),
    )
    inequality_dicts += [result_dict]
    return

def process_equality(expressions):
    global equality_dicts
    left_side_factor = 1
    right_side_factor = -1
    result_dict = merge_dicts(
        dict1=process_expression(expressions[0], left_side_factor, {}),
        dict2=process_expression(expressions[1], right_side_factor, {}),
    )
    equality_dicts += [result_dict]
    return

def process_line(line):
    global min_or_max_problem
    if MIN_SIGN in line:
        if not min_or_max_problem == None:
            return MORE_THAN_ONE_TARGET_FUNCTION
        min_or_max_problem = MIN
        process_target_function(line.split(MIN_SIGN)[1], MIN)
    elif MAX_SIGN in line:
        if not min_or_max_problem == None:
            return MORE_THAN_ONE_TARGET_FUNCTION
        min_or_max_problem = MAX
        process_target_function(line.split(MAX_SIGN)[1], MAX)
    elif GREATER_THAN_SIGN in line:
        process_inequality(line.split(GREATER_THAN_SIGN), GREATER_THAN)
    elif LOWER_THAN_SIGN in line:
        process_inequality(line.split(LOWER_THAN_SIGN), LOWER_THAN)
    elif EQUAL_SIGN in line:
        process_equality(line.split(EQUAL_SIGN))

def produce_scipy_input():
    f = open(INPUT_FILE, "r")
    for line in f:
        process_line(line.strip())
    return process_dicts()
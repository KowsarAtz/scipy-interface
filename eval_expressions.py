from constants import *

variables = []
inequality_dicts = []
equality_dicts = []
target_function_dict = {}
min_or_max_problem = None
minus_one = {
    CONSTANT_VALUE: -1
}

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


def mult_dicts(dict1, dict2):
    dict3 = None
    dict_const = None
    dict_modify = None
    if len(dict1.keys()) == 1 and (CONSTANT_VALUE in dict1.keys()):
        dict_const = dict1
        dict_modify = dict2
    elif len(dict2.keys()) == 1 and (CONSTANT_VALUE in dict2.keys()):
        dict_modify = dict1
        dict_const = dict2
    else:
        # RAISE ERROR (NON-LINEAR)
        return
    dict3 = dict_modify.copy()
    for key in dict3.keys():
        dict3[key] *= dict_const[CONSTANT_VALUE]
    return dict3

def p_closed_position(str_, start):
    i = -1
    chars = list(str_)
    if not chars[start] == '(':
        return NOT_FOUND # RAISE ERROR (INVALID USE OF FUNCTION)
    temp = 1
    for i in range(start+1, len(chars)):
        char = chars[i]
        if char == '(':
            temp+=1
        elif char == ')':
            temp-=1
            if temp == 0:
                return i
    return NOT_FOUND

def first_free_sign_position(str_, start, sign_):
    i = -1
    chars = list(str_)
    temp = 0
    for i in range(start, len(chars)):
        char = chars[i]
        if char == '(':
            temp+=1
        elif char == ')':
            temp-=1
        elif char == sign_ and temp == 0:
            return i
    return NOT_FOUND

def process_expression(expression):
    if expression == '':
        return {}

    if expression.find('(') == 0:
        i = p_closed_position(expression, 0)
        p1 = process_expression(expression[1:i])
        if i == len(expression) - 1:
            return p1
        
        j = first_free_sign_position(expression, i+1, SUM_SIGN)
        k = first_free_sign_position(expression, i+1, MULT_SIGN)
        if not j == NOT_FOUND:
            if j == i+1:
                return merge_dicts (
                    p1,
                    process_expression(expression[i+2:]),
                )
            elif k == i+1:
                temp = mult_dicts (
                    p1,
                    process_expression(expression[i+2:j]),
                )
                return merge_dicts (
                    temp,
                    process_expression(expression[j+1:])
                )
        if not k == NOT_FOUND and k == i+1:
            return mult_dicts (
                p1,
                process_expression(expression[i+2:])
            )
        return # RAISE ERROR (?)

    break_point = first_free_sign_position(expression, 0, SUM_SIGN)
    if not break_point == NOT_FOUND:
        return merge_dicts(
            process_expression(expression[0:break_point]),
            process_expression(expression[break_point+1:])
        )

    break_point = first_free_sign_position(expression, 0, MULT_SIGN)
    if not break_point == NOT_FOUND:
        return mult_dicts(
            process_expression(expression[0:break_point]),
            process_expression(expression[break_point+1:])
        )
    
    if DIVIS_SIGN in expression:
        return {
            CONSTANT_VALUE: eval(expression)
        }

    temp_val = None
    try:
        temp_val = float(expression)
    except ValueError:
        add_variable(expression)
        return {
            expression: 1
        }    
    
    return {
        CONSTANT_VALUE: temp_val
    }

refine_dict = (lambda x,factor: mult_dicts(minus_one, x) if factor == -1 else x)

def process_target_function(expression, type_):
    global target_function_dict
    target_function_dict = refine_dict(process_expression(expression), type_)


def process_inequality(expressions, type_):
    global inequality_dicts
    left_side_factor = type_
    right_side_factor = -1 * type_
    result_dict = merge_dicts(
        dict1=refine_dict(process_expression(expressions[0]), left_side_factor),
        dict2=refine_dict(process_expression(expressions[1]), right_side_factor)
    )
    inequality_dicts += [result_dict]
    return


def process_equality(expressions):
    global equality_dicts
    left_side_factor = 1
    right_side_factor = -1
    result_dict = merge_dicts(
        dict1=refine_dict(process_expression(expressions[0]), left_side_factor),
        dict2=refine_dict(process_expression(expressions[1]), right_side_factor)
    )
    equality_dicts += [result_dict]
    return


def process_line(line):
    global min_or_max_problem
    line = line.replace('-', '+(-1)*')
    line = line.replace(' ', '')
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


def produce_scipy_input(input_file=INPUT_FILE):
    f = open(input_file, "r")
    for line in f:
        process_line(line.strip())
    return process_dicts()

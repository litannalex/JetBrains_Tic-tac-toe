from re import fullmatch
from re import split as resplit
from re import findall
from string import ascii_letters
from collections import deque


def parse_command(command):
    # check if command exits and run it
    valid_commands = ['/exit', '/help']
    try:
        index = valid_commands.index(command)
    except Exception:
        print('Unknown command')
    else:
        if index == 0:
            print('Bye!')
            exit()
        elif index == 1:
            print('Welcome to Smart Calculator! You can add, subtract, multiply, or divide integers.\n'
                  'Also you can create variables and use them in your expression. Var names can be letters or words.\n'
                  'Parentheses work! Multiple plus/minus signs work!\n'
                  'To exit the calculator use \'/exit\' command.')


def parse_variable(user_input):
    user_var = resplit(' *= *', user_input)

    # check the var name for validity, returns dictionary with variables
    for char in user_var[0]:
        if char not in ascii_letters:
            print('Invalid identifier')
            return

    # check if more than 1 '=' signs
    if len(user_var) != 2:
        print('Invalid assignment1')
        return

    # check if new var value is existing var
    if user_var[1] in variables:
        variables[user_var[0]] = variables[user_var[1]]
    else:
        try:
            variables[user_var[0]] = int(user_var[1])
        except ValueError:
            print('Invalid assignment2')


def parse_expression(string_expression):
    contains_numeric = False
    # handles exceptions for expressions. should be integers/vars with operations and parentheses
    # permitted_operations = ('+', '-', '*', '/')
    # 1. String parsed to list using regex
    parsed = findall(r'[()]|-?\d*\.?\d+|[a-zA-Z]+|-+|\++|\*+|/+', string_expression)
    # 2. Checks that parentheses used correctly
    if check_parentheses(string_expression):
        # 3. Checks that operators used correctly
        for i in range(len(parsed)):
            if parsed[i] == '(' or parsed[i] == ')':
                continue
            elif fullmatch(r'[+-/*]+', parsed[i]) and i != len(parsed) - 1:
                o = parse_operation(parsed[i])
                if o is not None:
                    parsed[i] = o
                else:
                    print('Invalid expression')
                    return None
            # 4. Checks that vars exist, get their values
            elif parsed[i].isalpha():
                v = get_var(parsed[i])
                if v is not None:
                    parsed[i] = str(v)
                    contains_numeric = True
                else:
                    print('Unknown variable')
                    return None
            # 5. Checks that numbers are integers
            elif check_int(parsed[i]):
                contains_numeric = True
            else:
                print('Invalid expression')
                return None

        # Error when no numbers in expression
        if not contains_numeric:
            print('Invalid expression')
            return None
        else:
            # Returns final expression containing integers as operands and '-+*/' as operators
            return parsed

    else:
        print('Invalid expression')
        return None


def get_var(var):
    if var in variables:
        return variables[var]
    else:
        return None


def check_parentheses(expression):
    stack = deque()
    for i in expression:
        if i == '(':
            stack.append(i)
        if i == ')':
            try:
                stack.pop()
            except IndexError:
                return False
    if not stack:
        return True
    else:
        return False


def parse_operation(token):
    set_sub = {'-'}
    set_sum = {'+'}
    signs = set(token)
    if signs == set_sum or (signs == set_sub and len(token) % 2 == 0):
        return '+'
    elif signs == set_sub and len(token) % 2 == 1:
        return '-'
    elif token == '*':
        return '*'
    elif token == '/':
        return '/'
    else:
        return None


def check_int(number_str):
    try:
        int(number_str)
    except ValueError:
        return False
    else:
        return True


def to_postfix(expression):
    mul_div = ('*', '/')
    add_sub = ('+', '-')
    operators = deque()
    postfix = []
    # parse expression from left to right
    # operands are directly written into postfix expression (postfix)
    # operators are pushed to stack and written to postfix according to their precedence
    for item in expression:
        if item.isalpha() or item.isnumeric():
            postfix.append(item)
        else:
            if not operators or item == '(':
                operators.append(item)
            elif operators[-1] == '(':
                operators.append(item)
            elif item == ')':
                while operators:
                    a = operators.pop()
                    if a == '(':
                        break
                    else:
                        postfix.append(a)
            elif item in mul_div and operators[-1] in add_sub:
                operators.append(item)
            elif item in add_sub and (operators[-1] in mul_div or operators[-1] in add_sub):
                while operators:
                    b = operators[-1]
                    if b in mul_div or b in add_sub:
                        postfix.append(operators.pop())
                    else:
                        break
                operators.append(item)
            elif item in mul_div and operators[-1] in mul_div:
                while operators:
                    c = operators[-1]
                    if c in mul_div:
                        postfix.append(operators.pop())
                    else:
                        break
                operators.append(item)
    while operators:
        postfix.append(operators.pop())
    return postfix


def postfix_eval(expression):
    evaluation = deque()
    for item in expression:
        if check_int(item):
            evaluation.append(item)
        else:
            b = int(evaluation.pop())
            a = int(evaluation.pop())
            if item == '*':
                evaluation.append(a * b)
            elif item == '/':
                evaluation.append(a / b)
            elif item == '+':
                evaluation.append(a + b)
            elif item == '-':
                evaluation.append(a - b)
            # not implemented
            # elif item == '^':
            #     evaluation.append(a ** b)
    return evaluation.pop()


variables = {}
while True:
    input_string = input().strip()
    if not input_string:
        continue

    # input parsing: either command, variable assignment, or expression evaluation
    if input_string.startswith('/'):
        parse_command(input_string)
    elif '=' in input_string:
        parse_variable(input_string)
    else:
        numbers = parse_expression(input_string)
        if numbers is not None:
            result = postfix_eval(to_postfix(numbers))
            print(result)
        else:
            continue

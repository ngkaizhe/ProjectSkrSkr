from arrai.arrai import Arrai
from arrai.basic_operations import is_vector
import re


# helper functions
def set_function_patterns() -> str:
    answer = '^'
    answer += '('

    key_list_list = list(functions_map_list.keys())
    key_list = []

    # let key_list dont contain tuple or list inside
    for keys in key_list_list:
        if isinstance(keys, tuple) is True:
            for key in keys:
                key_list.append(key)
        else:
            key_list.append(keys)

    isFirst = True
    key_list = sorted(key_list, key=lambda element: len(element), reverse=True)
    for key in key_list:
        if isFirst:
            answer += key
            isFirst = False

        else:
            answer += '|' + key

    answer += ')'
    return answer

def MyMul(first: Arrai, second: Arrai):
    if is_vector(first) and is_vector(second):
        return first * second.transpose()
    else:
        return first * second

class Function(object):

    def __init__(self, name: str, function=None, total_variables=0):
        self.name = name
        self.function = function
        self.total_variables = total_variables

    def run_function(self, variables: list):
        if self.total_variables == 1:
            temp_answer = self.function(variables[0])

        elif self.total_variables == 2:
            temp_answer = self.function(variables[0], variables[1])

        elif self.total_variables == 3:
            temp_answer = self.function(variables[0], variables[1], variables[2])

        else:
            # TODO: if the function needs too much variables, considered pass in list
            pass

        return temp_answer

# {
# operator_string: [operator_TODO, precendence]
# }
operator_map_list = {
    '+': [Function('add', Arrai.__add__, 2), 1],
    '-': [Function('sub', Arrai.__sub__, 2), 1],
    '*': [Function('mul', MyMul, 2), 2],
    '\\': [Function('div', float.__divmod__, 2), 2],
}

# {
# operator_string: [function_TODO, precendence]
# }
functions_map_list = {
    ('Norm', 'norm'): [Function('Norm|norm', Arrai.norm, 1), 3],
    ('Normal', 'normal'): [Function('Normal|normal', Arrai.normal, 1), 3],
    'Rank': [Function('Rank', None, 1), 3],
    ('Cross', 'cross'): [Function('Cross|cross', Arrai.cross_product, 2), 3],
    ('Com', 'com'): [Function('Com|com', Arrai.component, 2), 3],
    ('Proj', 'proj'): [Function('Proj|proj', Arrai.projection, 2), 3],
    ('Area', 'area'): [Function('Area|area', Arrai.triangle_area, 2), 3],
}

class UIManager(object):

    def __init__(self):
        self.arrai_list: list
        self.recycle_bin: list
        """
        map_list = {
            'Operator/Function': {
                functions map list or operators map list
            }
        }
        """
        self.map_list: dict
        self.set_map_list()

        """
        precendences = {
            'operator symbols or function names': precendence
        }
        """
        self.precendences: dict
        self.set_precendences()

        """
        RPN = [
        ['string_token', 'type_token']
        ]
        """
        self.RPN: list

    def set_arrais(self, text_string: str) -> None:
        self.arrai_list = []
        self.recycle_bin = []

        text_string_list = text_string.splitlines()

        currentPos = 1
        for x in range(int(text_string_list[0])):
            VectorOrMatrix = text_string_list[currentPos]
            currentPos += 1

            if VectorOrMatrix == 'V':
                total = int(text_string_list[currentPos])
                currentPos += 1

                temp_list = text_string_list[currentPos].split(maxsplit=total)
                currentPos += 1

                temp_list = list(map(int, temp_list))
                self.arrai_list.append(Arrai(temp_list))

            elif VectorOrMatrix == 'M':
                (rows, cols) = list(map(int, text_string_list[currentPos].split()))
                currentPos += 1
                arrai = []

                for r in range(rows):
                    temp_list = text_string_list[currentPos].split(maxsplit=cols)
                    currentPos += 1
                    temp_list = list(map(int, temp_list))
                    arrai.append(temp_list)

                self.arrai_list.append(Arrai(arrai))

    def run_result(self, text_string: str) -> str:
        text_list = text_string.splitlines()

        for problem in text_list:
            self.build_RPN(problem)
            answer: Arrai = self.calculate_RPN()
            answer_string = self.get_string(answer)

            return answer_string

    def build_RPN(self, problem: str) -> None:
        if problem is None or problem == '':
            return
        """
        token_pieces = [
        [string_token, token_type]
        ]
        """
        token_pieces = self.seperate_problem(problem)
        """
        output = [
        [string_token, token_type]
        ]
        """
        output: list = []
        """
        stack = [
        [string_token, token_type, precendences]
        ]
        """
        stack: list = []

        for i in token_pieces:
            type = i[1]
            if type == 'Variable' or type == 'Number':
                output.append(i)

            elif type == 'Special':
                # only contains 3 characters here: '(', ',', ')'
                if i[0] == '(':
                    precendence = self.precendences[i[0]]
                    i.append(precendence)
                    stack.append(i)
                    output.append(i[0:2])

                elif i[0] == ',' or i[0] == ')':
                    left_parenthesis_found = False

                    while len(stack):
                        if stack[-1][0] != '(':
                            last_element = stack.pop()
                            output.append(last_element[0:2])

                        else:
                            if i[0] == ')':
                                stack.pop()
                                output.append(i)

                            left_parenthesis_found = True
                            break

                    # unexpected condition as comma or right parenthesis must have left parenthesis in front of them
                    if left_parenthesis_found is False:
                        print("Needed left parenthesis not found!")

                # unexpected condition
                else:
                    print("Invalid characters with special type detected!")

            elif type == 'Operator' or type == 'Function':
                precendence = self.precendences[i[0]]

                while len(stack):
                    # special case to be considered(left parenthesis only can be pop by right parenthesis)
                    if precendence <= stack[-1][2] and stack[-1][0] != '(':
                        last_element = stack.pop()
                        # dont take away precendence as it will not be used in future operation
                        output.append(last_element[0:2])

                    else:
                        break

                i.append(precendence)
                stack.append(i)

            # unexpected condition
            else:
                print("Invalid type detected inside token pieces!")
                return

        while len(stack):
            # expected condition as left parenthesis should be pop out when meeting right parenthesis,
            # if it remains left parenthesis, means that the counts of right parenthesis is longer than left parenthesis
            if stack[-1][0] == '(':
                print('Total number of right parenthesis is larger than left parenthesis!')

            last_element = stack.pop()
            output.append(last_element[0:2])

        self.RPN = output

    def seperate_problem(self, problem: str) -> list:
        problem_pieces = []
        # only separates the problem string into a list which contains operators, functions, and variables
        total_length = len(problem)
        start = 0

        # set patterns of difference types
        function_patterns: str = set_function_patterns()
        operator_patterns: str = '^[-\\\\+*]'
        variable_patterns: str = '^[a-zA-Z]'
        special_patterns: str = '^[(,)]'
        number_patterns: str = '^\d+[.]?\d*'

        while (start < total_length):
            if re.search(function_patterns, problem[start:]):
                match_object = re.search(function_patterns, problem[start:])
                start += len(match_object.group())
                function_string = match_object.group()
                problem_pieces.append([function_string, 'Function'])

            elif re.search(operator_patterns, problem[start:]):
                match_object = re.search(operator_patterns, problem[start:])
                start += len(match_object.group())
                problem_pieces.append([match_object.group(), 'Operator'])

            elif re.search(variable_patterns, problem[start:]):
                match_object = re.search(variable_patterns, problem[start:])
                start += len(match_object.group())
                problem_pieces.append([match_object.group(), 'Variable'])

            elif re.search(special_patterns, problem[start:]):
                match_object = re.search(special_patterns, problem[start:])
                start += len(match_object.group())
                problem_pieces.append([match_object.group(), 'Special'])

            elif re.search(number_patterns, problem[start:]):
                match_object = re.search(number_patterns, problem[start:])
                start += len(match_object.group())
                problem_pieces.append([match_object.group(), 'Number'])

            # whitespace cut off
            elif re.search('^(\s)', problem[start:]):
                start += 1

        return problem_pieces

    def set_map_list(self) -> None:
        # initialize
        self.map_list = {}

        self.map_list['Operator'] = operator_map_list

        self.map_list['Function'] = {}

        for key in functions_map_list.keys():
            if isinstance(key, tuple):
                for single_key in key:
                    self.map_list['Function'][single_key] = functions_map_list[key]

            else:
                self.map_list['Function'][key] = functions_map_list[key]

    def set_precendences(self) -> None:
        self.precendences = {}

        # set precendences of operators
        for (key, value) in self.map_list['Operator'].items():
            self.precendences.update({key: value[1]})

        # all function has the precendence 3
        for key in self.map_list['Function'].keys():
            if isinstance(key, tuple) is True:
                self.precendences.update(dict.fromkeys(key, 3))
            else:
                self.precendences.update({key: 3})

        # '(' has the highest precendence 10
        self.precendences.update({'(': 10})

    def calculate_RPN(self) -> Arrai:
        # cut off some parenthesises, only remains parenthesis that followed by function type token
        i = 0
        while i < len(self.RPN):
            if self.RPN[i][0] == ')':
                if self.RPN[i+1][1] != 'Function':
                    # find the corresponding left parenthesis position
                    j = i
                    while self.RPN[j][0] != '(' and j >= 0:
                        j -= 1

                    self.RPN.pop(i)
                    self.RPN.pop(j)
                    # 2 elements removed
                    i -= 2
            i += 1

        # replace variables type token to the proper value
        # which is a = the first arrai, b = the second arrai etc...
        length = len(self.RPN)
        total = 0
        for i in range(length):
            if self.RPN[i][1] == 'Variable':
                total += 1
                temp_char = self.RPN[i][0]
                pos = ord(temp_char) - ord('a')
                self.RPN[i][0] = self.arrai_list[pos]
                self.RPN[i][1] = 'Arrai'

            elif self.RPN[i][1] == 'Number':
                temp_number = float(self.RPN[i][0])
                self.RPN[i][0] = Arrai(temp_number)
                self.RPN[i][1] = 'Arrai'

        # delete the value inside arrai_list as will not be used in future
        self.recycle_bin.append(self.arrai_list[:total])
        del self.arrai_list[:total]

        # As all variables or number has been replace as Arrai, now the type
        # inside self.RPN should only be Arrai, Function, Operator
        # calculate the result
        i = 0
        while i < len(self.RPN):
            # all operators only used 2 operand
            if self.RPN[i][1] == 'Operator':
                if i < 2:
                    print('No operands in front of ' + self.RPN[i][0] + ' operator!')
                    return None

                operator_string = self.RPN[i][0]
                funct = self.map_list['Operator'][operator_string][0].function
                first = self.RPN[i-2][0]
                second = self.RPN[i-1][0]
                temp_arrai = funct(first, second)

                self.RPN[i][0] = temp_arrai
                self.RPN[i][1] = 'Arrai'
                del self.RPN[i-2:i]
                i -= 2

            elif self.RPN[i][1] == 'Function':
                """
                if function detected, it will fine the variables inside the RPN with using bracket!
                if the total variables isn't same with the total parameters the function needed, will throw exception
                """
                # get function
                function_string = self.RPN[i][0]
                function_type = self.map_list['Function'][function_string][0]

                # check the token before function was ')'
                if self.RPN[i-1][0] != ')' or i-1 < 0:
                    print('Function must followed before () bracket!')

                # get variables needed
                j = i-1
                left_bracket_found = False
                temp_variables = []
                temp_answer = None

                while j >= 0:
                    if self.RPN[j][0] == '(':
                        left_bracket_found = True
                        break

                    elif self.RPN[j][1] == 'Arrai':
                        temp_variables.append(self.RPN[j][0])

                    j -= 1

                if left_bracket_found is False:
                    print('Function must followed before () bracket!')

                if len(temp_variables) != function_type.total_variables:
                    print('Total Function Variables Needed not same as input variables!')

                else:
                    # remember to pass in the reversed variables
                    temp_answer = function_type.run_function(temp_variables[::-1])

                #replace the current RPN[i][0] with temp_answer
                self.RPN[i][0] = temp_answer
                self.RPN[i][1] = 'Arrai'

                del self.RPN[j:i]
                i -= (i-j+1)

            i += 1

        # As recycle_bin only for debugging purpose, clear it after every single line problem!
        self.recycle_bin = []

        if self.RPN[0]:
            return self.RPN[0][0]
        else:
            return None

    def get_string(self, arrai: (Arrai, int, float))->str:
        answer_string = ''
        if isinstance(arrai, Arrai):
            for i in arrai.array:
                if i is not None:
                    for j in i:
                        answer_string += str(j) + '\t'

                    answer_string = answer_string[:-1]
                    answer_string += '\n'
        elif isinstance(arrai, (int, float)):
            answer_string += str(arrai)

        return answer_string


if __name__ == '__main__':
    uimanager = UIManager()

    print_answer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    all_answers = []

    # V1.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V1.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('a+b+c+d'))
    answers.append(uimanager.run_result('(a+b)*c*d'))
    answers.append(uimanager.run_result('(a+b+c+d+e)*f'))
    all_answers.append(answers)
    if print_answer[0]:
        for i in answers:
            print(i)

        print('\n')

    # V2.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V2.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('a*b'))
    answers.append(uimanager.run_result('a*b'))
    answers.append(uimanager.run_result('a*b'))
    all_answers.append(answers)
    if print_answer[1]:
        for i in answers:
            print(i)

        print('\n')

    # V3.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V3.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('a+b'))
    answers.append(uimanager.run_result('a+b'))
    answers.append(uimanager.run_result('a+b'))
    all_answers.append(answers)
    if print_answer[2]:
        for i in answers:
            print(i)

        print('\n')

    # V4.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V4.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('a*b'))
    answers.append(uimanager.run_result('a*b'))
    answers.append(uimanager.run_result('a*b'))
    all_answers.append(answers)
    if print_answer[3]:
        for i in answers:
            print(i)

        print('\n')

    # V5.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V5.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('norm(a)'))
    answers.append(uimanager.run_result('Norm(a)'))
    answers.append(uimanager.run_result('norm(a)'))
    all_answers.append(answers)
    if print_answer[4]:
        for i in answers:
            print(i)

        print('\n')

    # V6.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V6.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('normal(a)'))
    answers.append(uimanager.run_result('Normal(a)'))
    answers.append(uimanager.run_result('normal(a)'))
    all_answers.append(answers)
    if print_answer[5]:
        for i in answers:
            print(i)

        print('\n')

    # V7.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V7.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('cross(a,b)'))
    answers.append(uimanager.run_result('Cross(a,b)'))
    answers.append(uimanager.run_result('Cross(a,b)'))
    all_answers.append(answers)
    if print_answer[6]:
        for i in answers:
            print(i)
        print('\n')

    # V8.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V8.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('com(a,b)'))
    answers.append(uimanager.run_result('Com(a,b)'))
    answers.append(uimanager.run_result('Com(a,b)'))
    all_answers.append(answers)
    if print_answer[7]:
        for i in answers:
            print(i)
        print('\n')

    # V9.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V9.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('proj(a,b)'))
    answers.append(uimanager.run_result('Proj(a,b)'))
    answers.append(uimanager.run_result('Proj(a,b)'))
    answers.append(uimanager.run_result('proj(a,b)'))
    all_answers.append(answers)
    if print_answer[8]:
        for i in answers:
            print(i)
        print('\n')

    # V10.txt
    filename = 'C:\\Users\\User\\Desktop\\Vector\\V10.txt'
    with open(filename, 'r') as file:
        read_data = file.read()
    uimanager.set_arrais(read_data)

    answers = []
    answers.append(uimanager.run_result('area(a,b)'))
    answers.append(uimanager.run_result('Area(a,b)'))
    answers.append(uimanager.run_result('Area(a,b)'))
    answers.append(uimanager.run_result('area(a,b)'))
    all_answers.append(answers)
    if print_answer[9]:
        for i in answers:
            print(i)
        print('\n')
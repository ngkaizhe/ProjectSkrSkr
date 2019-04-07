from arrai import Arrai
import re

class Function(object):

    def __init__(self, name: str, function=None, total_variables=None):
        self.name = name
        self.function = function
        self.total_variables = total_variables

    def get_result(self, *arguments):
        if self.function:
            return self.function(*arguments)

# {
# operator_string: [operator_TODO, precendence]
# }
operator_map_list = {
    '+': [Function('add', float.__add__), 1],
    '-': [Function('sub', float.__sub__), 1],
    '*': [Function('mul', float.__mul__), 2],
    '\\': [Function('div', float.__divmod__), 2],
}

functions_map_list = {
    ('Norm', 'norm'): [Function('Norm|norm', None)],
    ('Normal', 'normal'): [Function('Normal|normal', None)],
    'Rank': [Function('Rank', None)],
}

class UIManager(object):

    def __init__(self):
        self.arrai_list: list
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
            build_RPN(problem)
            answer = self.calculate_RPN()

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
        self.map_list = {
            'Operator': operator_map_list,
            'Function': functions_map_list,
        }

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

    def calculate_RPN(self) -> str:
        pass

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


if __name__ == '__main__':
    uimanager = UIManager()
    # uimanager.build_RPN('normal(norm(1+a+b*c))')
    # uimanager.build_RPN('normal(a, b)')
    # uimanager.build_RPN('A + B * C + D')
    # uimanager.build_RPN('(A + B) * (C + D)')
    # uimanager.build_RPN('A * B + C * D')
    # uimanager.build_RPN('A + B + C + D')
    uimanager.build_RPN('10 + 3 * 5 \ (16 - 4)')
    uimanager.build_RPN('( A + B ) * C - ( D - E ) * ( F + G )')

    a = 1
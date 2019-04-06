from arrai import Arrai
import re


class Function(object):

    def __init__(self, name, function = None):
        self.name = name
        self.function = function

    def get_result(self, *arguments):
        if self.function:
            return self.function(*arguments)


operator_map_list = {
    '+': [Function('add', float.__add__), ],
    '-': [Function('sub', float.__sub__), ],
    '*': [Function('mul', float.__mul__), ],
}

operators_precedence = {
    ('+', '-') : 1,
    ('*', '\\'): 2,
}

functions_map_list = {
    'Norm': [Function('Norm|norm', )],
    'Normal': [Function('Normal|normal', )],
}

class UIManager(object):

    def __init__(self):
        self.arrai_list: list
        self.functions_map_list = functions_map_list
        self.problem_pieces: list

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
            pass

    def build_RPN(self, problem: str) -> None:
        self.seperate_problem(problem)


    def seperate_problem(self, problem: str) -> None:
        self.problem_pieces = []
        # only separates the problem string into a list which contains operators, functions, and variables
        total_length = len(problem)
        start = 0

        # set patterns of difference types
        function_patterns: str = '^(normal|norm)'
        operator_patterns: str = '^[-\\+*]'
        variable_patterns: str = '^[a-z]'
        special_patterns: str = '^[(,)]'
        number_patterns: str = '^\d+[.]?\d*'

        while (start < total_length):
            if re.search(function_patterns, problem[start:]):
                match_object = re.search(function_patterns, problem[start:])
                start += len(match_object.group())
                self.problem_pieces.append([match_object.group(), 'function'])

            elif re.search(operator_patterns, problem[start:]):
                match_object = re.search(operator_patterns, problem[start:])
                start += len(match_object.group())
                self.problem_pieces.append([match_object.group(), 'operator'])

            elif re.search(variable_patterns, problem[start:]):
                match_object = re.search(variable_patterns, problem[start:])
                start += len(match_object.group())
                self.problem_pieces.append([match_object.group(), 'variable'])

            elif re.search(special_patterns, problem[start:]):
                match_object = re.search(special_patterns, problem[start:])
                start += len(match_object.group())
                self.problem_pieces.append([match_object.group(), 'special'])

            elif re.search(number_patterns, problem[start:]):
                match_object = re.search(number_patterns, problem[start:])
                start += len(match_object.group())
                self.problem_pieces.append([match_object.group(), 'number'])

            # whitespace cut off
            elif re.search('^(\s)', problem[start:]):
                start += 1

        return

if __name__ == '__main__':
    uimanager = UIManager()
    uimanager.build_RPN('normal(norm(1+a+b*c))')
    uimanager.build_RPN('normal(a, b)')
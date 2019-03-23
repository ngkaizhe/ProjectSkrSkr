class Matrix(object):
    """description of class"""

    # the input matrix should be one dimension list,
    # if the input matrix is in 2 dimension, then the isMatrix should be True
    def __init__(self, matrix: list, rows: int = None, cols: int = None) -> None:
        self.matrix = []

        # type checking
        # if illegal passing through value
        if not self.type_checking(matrix, rows, cols):
            # TODO: illegal type pass back exceptions
            print('Thread found')
            return

        # not 1d
        elif isinstance(matrix[0], list):
            # all conditions has been considered
            self.matrix = matrix

        # 1d
        else:
            # # normal C version
            # for i in range(rows):
            #    temp = []
            #    for j in range(cols):
            #        temp.append(matrix[i * cols + j])
            
            #    self.matrix.append(temp)

            # python version
            self.matrix = [[matrix[i * cols + j] for j in range(cols)] for i in range(rows)]

    # matrix addition
    def __add__(self, other) -> 'Matrix':
        # TODO: add exception(exception class still not yet created)

        # C++ version1
        # for i in range(len(self.matrix)):
        #    temp = []
        #    for j in range(len(self.matrix[i])):
        #        temp.append(self.matrix[i][j] + other.matrix[i][j])
        #    answer.append(temp)

        # c++ version2 using zip
        # for rows_self, rows_other in zip(self.matrix, other.matrix):
        #    temp = []
        #    for value_self, value_other in zip(rows_self, rows_other):
        #        temp.append(value_self + value_other)
        #    answer.append(temp)

        # # python version
        answer = [[value_self + value_other for value_self, value_other in zip(rows_self, rows_other)]for rows_self, rows_other in zip(self.matrix, other.matrix)]           
        return Matrix(answer)
    
    # matrix subtraction
    def __sub__(self, other) -> 'Matrix':
        # TODO: add exception(exception class still not yet created)

        # C++ version1
        # for i in range(len(self.matrix)):
        #    temp = []
        #    for j in range(len(self.matrix[i])):
        #        temp.append(self.matrix[i][j] - other.matrix[i][j])
        #    answer.append(temp)

        # c++ version2 using zip
        # for rows_self, rows_other in zip(self.matrix, other.matrix):
        #    temp = []
        #    for value_self, value_other in zip(rows_self, rows_other):
        #        temp.append(value_self - value_other)
        #    answer.append(temp)

        # # python version
        answer = [[value_self - value_other for value_self, value_other in zip(rows_self, rows_other)]for rows_self, rows_other in zip(self.matrix, other.matrix)]           
        return Matrix(answer)

    # matrix multiplication
    def __mul__(self, other) -> 'Matrix':
        # TODO: add exception(exception class still not yet created)

        answer = []
        # c++ version
        for i in range(len(self.matrix)):
            temp = []
            for j in range(len(other.matrix[0])):
                total = 0         
                for k in range(len(self.matrix[i])):
                    total += self.matrix[i][k] * other.matrix[k][j]
                temp.append(total)
            answer.append(temp)

        return Matrix(answer)

    # matrix rank
    def rank(self) -> int:
        pass

    # matrix transpose
    def transpose(self) -> 'Matrix':
        answer = [[row[i] for row in self.matrix] for i in range(len(self.matrix[0]))]
        return Matrix(answer)

    def print_value(self):
        for i in self.matrix:
            print(i)

    @staticmethod
    # this function will check if matrix is list
    def type_checking(matrix: list, rows: int = None, cols: int = None) -> bool:

        # check whether it is a list
        if not isinstance(matrix, list):
            return False

        # not 1d type checking
        elif isinstance(matrix[0], list):
            # if user pass in the rows and cols, constructor will check whether it is true or not
            if rows is not None and cols is not None:
                if len(matrix) != rows | len(matrix[0]) != cols:
                    # different rows and cols value against passed in matrix, return False
                    return False

            # check whether all element inside the list is list
            for i in matrix:
                if not isinstance(i, list):
                    # some elements inside matrix was not list, return False
                    return False
                for j in i:
                    if not (isinstance(j, int) or isinstance(j, float)):
                        # some elements inside i was not integer or float, return False
                        return False

        # 1d type checking
        else:
            # check the value and type of rows and cols
            if rows is None and cols is None:
                # the rows or cols is None, return False
                return False

            else:
                if not (isinstance(rows, int) and isinstance(cols, int)):
                    # type of rows and cols is not int, return False
                    return False

            # check all elements inside the given matrix is int or float
            for i in matrix:
                if not (isinstance(i, int) or isinstance(i, float)):
                    # type of element inside matrix is not float or int, return False
                    return False

            if len(matrix) != rows * cols:
                # the total length of 1d matrix was not same as rows * cols, return False
                return False

        # all conditions have been checked
        return True


if __name__ == "__main__":
    mat = Matrix([1, 10, 5, 7, 8, 7, 10, 11], 2, 4)
    mat2 = Matrix([1, 5, 4, 6, 7, 3, 6, 4, 2, 2, -1, 1], 4, 3)

    (mat * mat2).print_value()


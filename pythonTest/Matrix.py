class Matrix(object):
    """description of class"""

    # the input matrix should be one dimension list,
    # if the input matrix is in 2 dimension, then the isMatrix should be True
    def __init__(self, matrix: list, rows: int = None, cols: int = None) -> None:
        self.matrix = []

        # type checking
        # if illegal passing through value
        if not self.type_checking(matrix):
            # TODO: illegal type pass back exceptions
            return

        # not 1d
        elif isinstance(matrix[0], list):

            # if user pass in the rows and cols, constructor will check whether it is true or not
            if rows is not None and cols is not None:
                if len(matrix) != rows | len(matrix[0]) != cols:
                    # TODO: different rows and cols value against passed in matrix, return exception
                    return

            # check whether all element inside the list is list(2d)
            for i in matrix:
                if not isinstance(matrix[i], list):
                    # TODO: some elements inside matrix was not list, return exception
                    return
                for j in matrix[i]:
                    if not (isinstance(matrix[i][j], int) and isinstance(matrix[i][j], float)):
                        # TODO: some elements inside matrix[i] was not integer or float, return exception
                        return

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
            if rows is not None and cols is not None:
                self.matrix = [[matrix[i * cols + j] for j in range(cols)] for i in range(rows)]

            else:
                # TODO: passing in a 1d array without passing value to rows and cols, return exception
                return

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

    # this function will check if matrix is list
    def type_checking(self, matrix: list) -> bool:

        # check whether it is a list
        if not isinstance(matrix, list):
            return False

        else:
            return True


if __name__== "__main__":
    mat = Matrix([1, 10, 5, 7, 8, 7, 10, 11], 2, 4)
    mat2 = Matrix([1, 5, 4, 6, 7, 3, 6, 4, 2, 2, -1, 1], 4, 3)

    (mat.transpose()).print_value()


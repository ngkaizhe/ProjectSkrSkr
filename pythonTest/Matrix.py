class Matrix(object):
    """description of class"""

    # the input matrix should be one dimension list,
    #if the input matrix is in 2 dimension, then the isMatrix should be True
    def __init__(self, matrix, rows = 0, cols = 0, isMatrix = False):
        self.matrix = []

        if isMatrix:
            self.matrix = matrix 

        else:
            ##normal C version
            #for i in range(rows):
            #    temp = []
            #    for j in range(cols):
            #        temp.append(matrix[i * cols + j])
            
            #    self.matrix.append(temp)

            #python version
            self.matrix = [[matrix[i * cols + j] for j in range(cols)] for i in range(rows)]

    #matrix addition
    def __add__(self, other):
        answer = []
        #C++ version1
        #for i in range(len(self.matrix)):
        #    temp = []
        #    for j in range(len(self.matrix[i])):
        #        temp.append(self.matrix[i][j] + other.matrix[i][j])
        #    answer.append(temp)

        #c++ version2 using zip
        #for rows_self, rows_other in zip(self.matrix, other.matrix):
        #    temp = []
        #    for value_self, value_other in zip(rows_self, rows_other):
        #        temp.append(value_self + value_other)
        #    answer.append(temp)

        ##python version
        answer = [[value_self + value_other for value_self, value_other in zip(rows_self, rows_other)]for rows_self, rows_other in zip(self.matrix, other.matrix)]           
        return Matrix(answer, isMatrix = True)
    


    def print_value(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i])
        


if __name__== "__main__":
    mat = Matrix([1, 10, 5, 7, 8, 7, 10, 11], 2, 4)
    mat2 = Matrix([1, 5, 6, 7, 6, 4, 2, -1], 2, 4)

    (mat+mat2).print_value()


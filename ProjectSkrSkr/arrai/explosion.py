from enum import Enum

"""
explosion.py

This is the exception class for arrai

"""

class Explosion(Enum):
    BLANK_ARRAY_PASS_IN = ValueError('Array requires to have something')
    INIT_ARGUMENT_TYPE_ERROR = TypeError("Argument must be of type list or numerical values(scalar)")
    INVALID_ARRAY_DIM = ValueError('Not a valid n * m array')
    INVALID_NUMERICAL_TYPE = ValueError("Element must be numerical values")
    INVALID_ARITHMETIC_OPERATOR = ValueError("Invalid Operator")
    INVALID_ARITHMETIC_OPERAND = ValueError("Invalid Operand")
    ARITHMETIC_SHAPE_MISMATCH = ValueError("Arithmetic requires both to be of same dimension or either one to be a scalar")
    SUM_SHAPE_MISMATCH = ValueError("Sum requires both to be of same dimension")
    DOT_SHAPE_MISMATCH = ValueError("Dot requires both to be of same dimension")
    DOT_DIM_MISMATCH = ValueError("Array dimension mismatched!")
    SWAP_DIM_EXCEED = ValueError("Swap Dim")
    SET_DIM_EXCEED = ValueError("Set Row")
    SET_INVALID_VECTOR = ValueError("Invalid Vector")
    CONVERT_NOT_VECTOR = ValueError("Not a vector to be converted")
    INVALID_ARGS_NOT_ARRAI = ValueError("Arguments must be arrai");
    INVERSE_NOT_SQUARE_ARRAI = ValueError("Matrix must be square inorder to find inverse")
    INVERSE_NOT_EXIST = ValueError("Inverse not exist, matrix not invertible")
    DET_NOT_SQUARE_ARRAI = ValueError("Matrix must be square inorder to find determinant")
    RESHAPE_DIMSIZE_MISMATCHED = ValueError("Reshape must be of the same size as the original arrai")
    RREF_ROWSIZE_MISMATCHED = ValueError("Row size must be some inorder to performs RREF")
    CROSS_PRODUCT_NOT_VECTOR = ValueError('Only vector could perform cross product')
    CROSS_PRODUCT_VECTOR_NOT_THREE_DIMENSION = ValueError('I only know how to perform cross product of vectors with 3 elements inside')
    COMPONENT_NOT_VECTOR = ValueError('I only know how to perform component using vectors')
    PROJECTION_NOT_VECTOR = ValueError('I only know how to perform projection using vectors')
    TRIANGLE_AREA_NOT_VECTOR = ValueError('I only know how to perform triangle area using vectors')
    TRIANGLE_AREA_VECTOR_NOT_SAME_DIMENSION = ValueError('I only know how to perform triangle area using same dimension\'s vectors')
    ANGLE_NOT_VECTOR = ValueError('I only know how to perform angle using vectors')
    ANGLE_VECTOR_NOT_SAME_DIMENSION = ValueError('I only know how to perform angle using same dimension\'s vectors')
    PARALLEL_NOT_VECTOR = ValueError('I only know how to find parallel using vectors')
    PARALLEL_VECTOR_NOT_SAME_DIMENSION = ValueError('I only know how to perform parallel using same dimension\'s vectors')
    ORTHOGONAL_NOT_VECTOR = ValueError('I only know how to find orthogonal using vectors')
    ORTHOGONAL_VECTOR_NOT_SAME_DIMENSION = ValueError('I only know how to perform orthogonal using same dimension\'s vectors')
    PLANE_NORMAL_NOT_VECTOR = ValueError('I only know how to find plane normal using vectors')
    PLANE_NORMAL_VECTOR_NOT_THREE_DIMENSION = ValueError(
        'I only know how to plane normal using 3 dimensions vectors')
    LINEAR_SYSTEM_ROW_NUM_NOT_EQUAL = ValueError("The row number of A and B must match in order to solve")
    LEAST_SQUARE_ROW_NUM_NOT_EQUAL = ValueError("The row number of A and B must match in order to get least square")
    POWER_METHOD_ITER_OVER_LIMIT = ValueError("Iteration over limit, the eigen value might be a complex number")
    EIGEN_ACOS_LARGER_ONE = ValueError("Q^3 greater than R^2, the eigen value might be a complex number")
    EIGEN_NOT_SQUARE = ValueError("The array must be square to solve for eigen value and vectors")
    EIGEN_DIM_NOT_SUPPORTED = ValueError("Eigen only support matrix of size 2*2 and 3*3 currently")
    NO_NULL_SPACE = ValueError("No null space")

    INPUT_INVALID = ValueError('Sorry, your input is invalid! Cant match some words!')

    TYPE_NOT_SUPPORTED = ValueError("Type Not supported")

    def bang(self, msg = ""):
        self.value.args = (self.value.args[0] +'\n' +msg,)
        raise self.value
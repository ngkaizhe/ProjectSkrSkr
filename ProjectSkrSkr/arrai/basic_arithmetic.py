from .arrai import *
from .explosion import Explosion
from .basic_operations import *

def basic_arithmetic(first: Arrai, second: Arrai, op: str):

    scalar = None

    if  is_scalar(first) or is_scalar(second):
        (scalar,arr) = (to_scalar(first),second) if is_scalar(first) else (to_scalar(second),first)

    elif not (isinstance(first, Arrai) and isinstance(second, Arrai)):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    if (op == '+'):      func_op = lambda x, y: x + y
    elif (op == '-'):    func_op = lambda x, y: x - y
    elif (op == '*'):    func_op = lambda x, y: x * y
    elif (op == '/'):    func_op = lambda x, y: x / y
    else:
        Explosion.INVALID_ARITHMETIC_OPERATOR.bang()


    mat = []

    if scalar is not None:
        if is_scalar(arr):
            return Arrai(func_op(scalar, to_scalar(arr)))
        else:
            for i in range(arr.shape[0]):
                row = []
                for j in range(arr.shape[1]):
                    # Performs element wise operation with scalar
                    row.append(func_op(arr[i][j], scalar)) 
                mat.append(row)
    else:
        if first.shape == second.shape:
            for row1, row2 in zip(first.array, second.array):
                row = []
                for x, y in zip(row1, row2):
                    # Performs element wise operation with x and y
                    row.append(func_op(x,y))
                mat.append(row)
        else: # Throw exception where the shape mismatched
            Explosion.ARITHMETIC_SHAPE_MISMATCH.bang()


    return Arrai(mat) 
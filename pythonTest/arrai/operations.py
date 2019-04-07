import copy

from .arrai import *
from .explosion import Explosion
from . import helpers as helpers

""" 
arrai_operation.py

Concrete module for array's operation such as transpose, inverse, arithmetic, etc

"""


def transpose(arr: Arrai) -> Arrai:
    ret = [[row[i] for row in arr.array] for i in range(arr.shape[1])]
    return Arrai(ret)

def to_RREF(arr: Arrai) -> Arrai: #(tuple(Arrai, Arrai))
    return helpers.helper_RREF(arr)["A"]

def inverse(arr: Arrai) -> Arrai:
    if not is_square(arr):
        Explosion.INVERSE_NOT_SQUARE_ARRAI.bang()
        return
    ret = helpers.helper_RREF(arr, Arrai.identity((arr.length(), arr.length())));
    if(ret["rank"] != arr.length()):
        Explosion.INVERSE_NOT_EXIST.bang()
        return 
    else:
        return ret["B"]

def rank(arr: Arrai) -> NumberTypes:
    return helpers.helper_RREF(arr)["rank"]

def det(arr: Arrai) -> NumberTypes:
    if not is_square(arr):
        Explosion.DET_NOT_SQUARE_ARRAI.bang()
        return
    return helpers.helper_RREF(arr)["det"]


    # helper func for basic arithmetic operation, element-wise

"""
Follow Matlab definition
sum is reserved by python for __+__, thus zum is used

For Vector:
return the summed value(scalar) of all element

For Matrix:
dim = 1: summation for all column vectors
dim = 2: summation for all row vectors
"""

from math import sqrt
def norm(arr: Arrai) -> NumberTypes:
    if not isinstance(arr, Arrai):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(is_vector(arr)):
        return sqrt(to_scalar(dot(arr, arr)))
    else:
        Explosion.TYPE_NOT_SUPPORTED.bang("normalization of matrix is not supported")
        # TODO

def normalize(arr: Arrai) -> Arrai:
    if not isinstance(arr, Arrai):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(is_vector(arr)):
        return arr / norm(arr)
    else:
        Explosion.TYPE_NOT_SUPPORTED.bang("normalization of matrix is not supported")
        # TODO




def zum(first: Arrai, dim = 1) -> Arrai:

    if not isinstance(first, Arrai):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    if(is_vector(first)): # Force sum into scalar if it is vector, as defined in matlab
        first = to_row_vector(first)
        dim = 2

    ret = []
    if(dim == 1):
        for i in range(first.shape[1]):
            total = 0
            for j in range(first.shape[0]): # Sum through all column vectors
                total += first[j][i]
            ret.append(total)

    elif(dim == 2):
        for i in range(first.shape[0]):
            total = 0
            for j in range(first.shape[1]): # Sum through all row vectors
                total += first[i][j]
            ret.append([total])

    return Arrai(ret)



def dot(first: Arrai, second: Arrai, dim = 1) -> Arrai:

    if not (isinstance(first, Arrai) and isinstance(second, Arrai)):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(is_vector(first) and is_vector(second)):
        if(first.length() == second.length()):
            return to_row_vector(first) * to_col_vector(second) # row vector by col vector

        else: Explosion.DOT_SHAPE_MISMATCH.bang() # Vector size mismatched

    elif(first.shape == second.shape):
        return zum(basic_arithmetic(first, second, '*'), dim)
    
    else:
        Explosion.DOT_SHAPE_MISMATCH.bang()



def mul(first: Arrai, second: Arrai) -> Arrai:

    if (is_scalar(first) or is_scalar(second)):
        return basic_arithmetic(first, second, '*')

    elif (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    if (first.shape[1] == second.shape[0]):

        mat = []

        for i in range(first.shape[0]):
            row = []
            for j in range(second.shape[1]):
                sum_product = 0         
                for k in range(first.shape[1]):
                    sum_product += first[i][k] * second[k][j]
                row.append(sum_product)
            mat.append(row)
        return Arrai(mat)

    else:
        Explosion.DOT_DIM_MISMATCH.bang()


def div(first: Arrai, second: Arrai) -> Arrai:
    if is_scalar(second):
        return basic_arithmetic(first, second, '/')

    if not isinstance(first, Arrai):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    else: # Matrix-Matrix Division
        #TODO? Should the checking be left to multiplication?
        return first * inverse(second)
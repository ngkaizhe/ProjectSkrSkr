import copy

from .arrai import *
from .explosion import Explosion
import math


def reshape(arr: Arrai, shape: (tuple, list)) -> Arrai:
    total = 1

    # shape can only contain 2 elements inside
    if len(shape) is not 2:
        # TODO: return exception
        return

    shape_list = shape
    # get the total value inside shape
    for i in shape_list:
        total *= i

    if total is not arr.shape[0] * arr.shape[1]:
        Explosion.RESHAPE_DIMSIZE_MISMATCHED.bang();
        return
    else:
        # change the array of self to 1d first
        one_dimension_array = combine_array(arr.array)

        # then starts the reshape job
        new_list = cut_array(one_dimension_array, shape_list, 0)

        return Arrai(new_list)

#Function to set row vector of index r of arr
def set_row(arr: Arrai, r: int, vec: Arrai) -> Arrai:
    if(r >= arr.shape[0]):
        Explosion.SET_DIM_EXCEED.bang()
        return
    if not is_vector(vec) or vec.length() != arr.shape[1]:
        Explosion.SET_INVALID_VECTOR.bang()
        return

    ret = copy.deepcopy(arr)
    vec = to_row_vector(vec) # Convert the vector into row vector to aid with the operation

    # Iterate throughout the row vector, concenate and assign
    ret.array[r] = [el for el in vec[0]]
    return ret

def delete_row(arr: Arrai, r: int = -1) -> Arrai:
    if(r == -1): r = arr.shape[0]-1
    elif(r >= arr.shape[0]):
        Explosion.SET_DIM_EXCEED.bang()
        return

    del arr.array[r]
    arr.shape[0] -= 1

    return arr

def delete_col(arr: Arrai, c: int = -1) -> Arrai:
    if (c == -1):
        c = arr.shape[1]-1
    elif (c >= arr.shape[1]):
        Explosion.SET_DIM_EXCEED.bang()
        return

    for i in range(len(arr.array)):
        del arr.array[i][c]

    arr.shape[1] -= 1;

    return arr

def insert_row(arr: Arrai, vec: Arrai, r: int = -1) -> Arrai:
    if(r == -1): r = arr.shape[0]
    elif(r > arr.shape[0]):
        Explosion.SET_DIM_EXCEED.bang()
        return
    if not is_vector(vec) or vec.length() != arr.shape[1]:
        Explosion.SET_INVALID_VECTOR.bang()
        return

    vec = to_row_vector(vec) # Convert the vector into row vector to aid with the operation

    arr.array.append([])
    for i in range(arr.shape[0], r-1, -1):
        arr.array[i] = arr.array[i-1]

    arr.array[r] = [el for el in vec[0]]
    arr.shape[0] += 1;

    return arr

def insert_col(arr: Arrai, vec: Arrai, c: int = -1) -> Arrai:
    if(c == -1): c = arr.shape[1]
    elif(c > arr.shape[1]):
        Explosion.SET_DIM_EXCEED.bang()
        return
    if not is_vector(vec) or vec.length() != arr.shape[0]:
        Explosion.SET_INVALID_VECTOR.bang()
        return

    vec = to_row_vector(vec)

    for i in range(len(arr.array)):
        arr.array[i].append(0)
        for j in range(arr.shape[1], c-1, -1):
            arr.array[i][j] = arr.array[i][j-1]

    for i in range(len(arr.array)):
        arr[i][c] = vec[0][i]

    arr.shape[1] += 1;
    
    return arr

# Function to set column vector of index c of arr
def set_col(arr: Arrai, c: int, vec: Arrai) -> Arrai:
    if(c >= arr.shape[1]):
        Explosion.SET_DIM_EXCEED.bang()
        return
    if not is_vector(vec) or vec.length() != arr.shape[0]:
        Explosion.SET_INVALID_VECTOR.bang()
        return

    ret = copy.deepcopy(arr)
    vec = to_row_vector(vec)

    # Iterate throughout the column vector and assign one by one
    for i in range(len(ret.array)):
        ret[i][c] = vec[0][i]

    return ret

# Function to convert vector to row vector
def to_row_vector(vec: Arrai) -> Arrai:
    if not is_vector(vec): 
        Explosion.CONVERT_NOT_VECTOR.bang()
    l = vec.length()
    if vec.shape[0] == l: # Is col vector
        return Arrai([i[0] for i in vec])
    else: # Is row vector
        return Arrai([i for i in vec[0]])

def to_col_vector(vec: Arrai) -> Arrai:
    if not is_vector(vec): 
        Explosion.CONVERT_NOT_VECTOR.bang()
    l = vec.length()
    if vec.shape[0] == l: # Is col vector
        return Arrai([[i[0]] for i in vec])
    else: # Is row vector
        return Arrai([[i] for i in vec[0]])

# Return a new Arrai with swapped rows
def swap_row(arr: Arrai, r1: int, r2: int) -> Arrai:
    if r1 >= arr.shape[0] or r2 >= arr.shape[0]:
        Explosion.SWAP_DIM_EXCEED.bang()
        return

    mat = copy.deepcopy(arr.array)
    mat[r1], mat[r2] = mat[r2], mat[r1]
    return Arrai(mat)

# Return a new Arrai with swapped columns
def swap_col(arr: Arrai, r1: int, r2: int) -> Arrai:
    if r1 >= arr.shape[1] or r2 >= arr.shape[1]:
        Explosion.SWAP_DIM_EXCEED.bang()
        return

    mat = copy.deepcopy(arr.array)
    for i in range(len(mat)):
        mat[i][r1], mat[i][r2] = mat[i][r2], mat[i][r1]
    return Arrai(mat)

def is_vector(object: Arrai) -> bool:
    if(isinstance(object, Arrai)):
        if(object.shape[0] == 1 or object.shape[1] == 1):
            return True
    return False

# Check whether it is scalr or not. applicaple for both NumberTypes and Arrai
def is_square(object: Arrai) -> bool:
    if(isinstance(object, Arrai)):
        if(object.shape[0] == object.shape[1]):
            return True
    return False 

def is_scalar(object: Arrai) -> bool:
    if(isinstance(object, NumberTypes)):
        return True
    elif(isinstance(object, Arrai)
        and (object.shape[0] is 1) and (object.shape[1] is 1)):
            return True
    
    return False

def is_zeros(object: Arrai) -> bool:
    if(isinstance(object, Arrai)):
        for i in object:
            for j in i:
                if not math.isclose(math.fabs(j), 0, abs_tol=ERROR): return False
        return True
    return False

# Return the scalar in numerical type if it is scalar
def to_scalar(object) -> NumberTypes:
    if(isinstance(object, NumberTypes)):
        return object
    elif(isinstance(object, Arrai) and is_scalar(object)):
        return object[0][0]
    
    return None
from recursive_functions import *
from enum import Enum
import copy

NumberTypes = (int, float, complex)

class Arrai(object):
    """description of class"""

    # instance methods
    # create an array

    def __init__(self, object: list) -> None:
        # attribute definition
        if (isinstance(object, list) is False
            and isinstance(object, int) is False
            and isinstance(object, float) is False):
                Explosion.INIT_ARGUMENT_TYPE_ERROR.bang()

        self.ndim = 0 # Number of array dimensions.
        self.shape = 0
        self.set_array(object)

    def __repr__(self):
        answer = 'Arrai('
        answer += get_string(self.array, self.ndim - 1, self.ndim, ',', True)
        answer += ')'
        return answer

    def __str__(self):
        answer = '\n'
        answer += get_string(self.array, self.ndim - 1, self.ndim, '  ', False)
        answer += '\n'

        return answer

    def __getitem__(self, index):
        return self.array[index]

    # Operator overloading
    def __add__(self, other):
        print(type(other))
        return basic_arithmetic(self, other, '+')

    def __radd__(self, other):
        return basic_arithmetic(self, other, '+')

    def __sub__(self, other):
        return basic_arithmetic(self, other, '-')

    def __rsub__(self, other):
        return basic_arithmetic(self, other, '-')

    def __mul__(self, other):
        return mul(self, other)

    def __rmul__(self, other):
        return mul(self, other)

    def __truediv__(self, other):
        return div(self, other)

    def reshape(self, shape: (tuple, list)):
        total = 1

        # shape can only contain 2 elements inside
        if len(shape) is not 2:
            # TODO: return exception
            return

        shape_list = shape
        # get the total value inside shape
        for i in shape_list:
            total *= i

        if self.size is not total:
            # TODO: return exception
            return
        else:
            # change the array of self to 1d first
            one_dimension_array = combine_array(self.array)

            # then starts the reshape job
            new_list = cut_array(one_dimension_array, shape_list, 0)

            return Arrai(new_list)

    @classmethod
    def ones(cls, shape: (tuple, list, int)):
        return cls.full(shape, 1)

    @classmethod
    def zeros(cls, shape: (tuple, list, int)):
        return cls.full(shape, 0)

    @classmethod
    def full(cls, shape: (tuple, list), value=0):
        List: list = []

        # shape can only contain 2 elements inside
        if len(shape) is not 2:
            # TODO: return exception
            return

        temp_list = value
        for x in reversed(shape):
            List.clear()
            for i in range(x):
                List.append(temp_list)
            temp_list = List[:]

        return cls(List)

    @classmethod
    def identity(cls, shape: (tuple, list)):

        List = []
        # only use for ndim = 2
        if len(shape) is 2:
            for i in range(shape[0]):
                temp_list = []
                for j in range(shape[1]):
                    if i is j:
                        temp_list.append(1)
                    else:
                        temp_list.append(0)
                List.append(temp_list)
            return cls(List)

        else:
            # TODO: return exception
            pass

    @classmethod
    def arange(cls, total: int):
        new_list = []
        for i in range(total):
            new_list.append(i)

        return cls(new_list)


    # static method
    # set up attribute part
    @staticmethod
    def get_ndim(object: list) -> int:

        ndim = 0
        element = object

        while isinstance(element, list) is True:
            element = element[0]
            ndim += 1
        return ndim

    @staticmethod
    def get_shape(object: list) -> int:

        shape = []
        element = object
        while isinstance(element, list) is True:
            shape.append(len(element))
            element = element[0]

        return shape

    def check_validity(self) -> None:
        if(self.ndim != 2):
            return
        for i in self.array:
            if(len(i) != self.shape[1]):
                Explosion.INVALID_ARRAY_DIM.bang()
            for j in i:
                if(not(isinstance(j, NumberTypes))):
                    Explosion.INVALID_NUMERICAL_TYPE.bang()

        return
        # check if this array is a valid array applicable

    def set_array(self, object: list) -> None:

        self.ndim = Arrai.get_ndim(object)
        # scalar passing inside, shape will be 1*1
        if self.ndim == 0:
            self.array = [[]]
            self[0].append(object)
            self.ndim = 2

        # vector passing inside/ 1D array
        elif self.ndim == 1:
            self.array = []
            self.array.append(object)
            self.ndim = 2

        # matrix/ 2D array passing inside
        elif self.ndim == 2:
            self.array = object

        else:
            
            self.array = None

        if(self.array == None):
            raise ValueError("array cannot be blank")
            #TODO : throw exceptions
        
        self.shape = Arrai.get_shape(self.array)
        Arrai.check_validity(self)

    def dot(self, other) -> 'Arrai':
        return dot(self, other)

    def mul(self, other) -> 'Arrai':
        return mul(self, other)

    def transpose(self) -> 'Arrai':
        return transpose(self)


    def row(self, index: int) -> 'Arrai':
        return Arrai(self.array[index])

    def col(self, index: int) -> 'Arrai':
        return Arrai([[self.array[i][index]] for i in range(self.shape[0])])

    def el(self, index: int) -> NumberTypes:
        if(index < self.shape[0] * self.shape[1]):
            return self[index / self.shape[1]][index % self.shape[1]]

    def length(self) -> int: # Length of largest array dimension
        return max(self.shape[0], self.shape[1])

    def set_row(self, r: int, vec: 'Arrai') -> 'Arrai':
        return set_row(self, r, vec)

    def set_col(self, r: int, vec: 'Arrai') -> 'Arrai':
        return set_col(self, c, vec)

    def swap_row(self, r1: int, r2: int) -> 'Arrai':
        return swap_row(self, r1, r2)

    def swap_col(self, r1: int, r2: int) -> 'Arrai':
        return swap_col(self, r1, r2)




    # Perform element wise arithmetic operation

    # https://rosettacode.org/wiki/Reduced_row_echelon_form for psudocode
    # Reduced Row Echelon Form 
    # will return a tuple(RREF, INVERSE) if inverse calculation is enabled
    # otherwise only RREF(of type Arrai) is returned
def to_RREF(arr: Arrai, f_calculate_inverse: bool = False) -> Arrai: #(tuple(Arrai, Arrai))

    if not isinstance(arr, Arrai):
        Explosion.INVALID_ARGS_NOT_ARRAI.bang()

    if(f_calculate_inverse):
        if not is_square(arr):
            f_calculate_inverse = False
            Explosion.INVERSE_NOT_SQUARE_ARRAI.bang()
        else:
            ret_inv = Arrai.identity((arr.length(), arr.length()))

    i_lead = 0 # Index of column vector in matrix
    row_count = arr.shape[0]
    col_count = arr.shape[1]

    ret = copy.deepcopy(arr)

    for r in range(row_count):
        if(i_lead >= col_count): return ret
        i = r
        while(ret[i][i_lead] == 0):
            i += 1
            if(i == row_count):
                i = r
                i_lead += 1
                if(i_lead == col_count): return ret
        ret = swap_row(ret, i, r)
        if(f_calculate_inverse): ret_inv = swap_row(ret_inv, i, r)

        if(ret[r][i_lead] != 0): # Make the lead to be 1 by dividing whole row by lead itself
            lead = ret[r][i_lead]
            ret = ret.set_row(r, ret.row(r) / lead);
            if(f_calculate_inverse): ret_inv = ret_inv.set_row(r, ret_inv.row(r) / lead);

        for i in range(row_count): # Elementary row operation to clean up columns
            if(i == r): continue
            lead = ret[i][i_lead]
            ret = ret.set_row(i, ret.row(i) - ret.row(r) * lead)
            if(f_calculate_inverse): ret_inv = ret_inv.set_row(i, ret_inv.row(i) - ret_inv.row(r) * lead);
        i_lead += 1
    if(f_calculate_inverse): return (ret, ret_inv)
    else: return ret



#Function to set row vector of index r of arr
def set_row(arr: Arrai, r: int, vec: Arrai) -> Arrai:
    if(r >= arr.shape[0]):
        Explosion.SET_DIM_EXCEED.bang()
        return
    if not is_vector(vec) or vec.length() != arr.shape[1]:
        Explosion.SET_INVALID_VECTOR.bang()
        return

    ret = copy.deepcopy(arr)
    vec = to_row_vector(vec)
    ret.array[r] = [el for el in vec[0]]
    return ret

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
    return transpose(to_row_vector(vec))


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


class Explosion(Enum):
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

    def bang(self):
        raise self.value


# helper func for basic arithmetic operation, element-wise
def basic_arithmetic(first: Arrai, second: Arrai, op: str):

    scalar = None

    if  is_scalar(first) or is_scalar(second):
        (scalar,arr) = (get_scalar(first),second) if is_scalar(first) else (get_scalar(second),first)

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
            return Arrai(func_op(scalar, get_scalar(arr)))
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



"""
Follow Matlab definition
sum is reserved for python, thus zum is used

dim = 1: summation for all column vectors
dim = 2: summation for all row vectors
"""
def zum(first: Arrai, second: Arrai = None, dim = 1) -> Arrai:

    if(second == None): 
        second = Arrai.zeros(first.shape)

    if (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(first.shape == second.shape):
        ret = []
        if(dim == 1):
            for i in range(first.shape[1]):
                total = 0
                for j in range(first.shape[0]): # Sum through all column vectors
                    total += first[j][i] + second[j][i] 
                ret.append(total)
        elif(dim == 2):
            for i in range(first.shape[0]):
                total = 0
                for j in range(first.shape[1]): # Sum through all column vectors
                    total += first[i][j] + second[i][j] 
                ret.append([total])
        return Arrai(ret)
    else:
        Explosion.SUM_SHAPE_MISMATCH.bang()



def dot(first: Arrai, second: Arrai, dim = 1) -> Arrai:

    if (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(is_vector(first) and is_vector(second)):
        if(first.shape[0] == 1 and first.shape[1] == second.shape[1]): # First is Row and Second is Row Vec
            return first * transpose(second)
        elif(first.shape[0] == 1 and first.shape[1] == second.shape[0]): # First is Row and Second is Col Vec
            return first * second
        elif(first.shape[1] == 1 and first.shape[0] == second.shape[0]): # First is Col and Second is Row Vec
            return second * transpose(first)
        elif(first.shape[1] == 1 and first.shape[0] == second.shape[1]): # First is Col and Second is Col Vec
            return  second * first
        else: Explosion.DOT_SHAPE_MISMATCH.bang() # Vector size mismatched

    elif(first.shape == second.shape):
        return zum(basic_arithmetic(first, second, '*'), dim = dim)
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

    else:
        return first * inverse(second)


def inverse(arr: Arrai) -> Arrai:
    out_inv = to_RREF(arr, f_calculate_inverse = True)[1]
    
    return out_inv

def transpose(arr: Arrai) -> Arrai:
    ret = [[row[i] for row in arr.array] for i in range(arr.shape[1])]
    return Arrai(ret)



def is_vector(object: Arrai):
    if(isinstance(object, Arrai)):
        if(object.shape[0] == 1 or object.shape[1] == 1):
            return True
    return False


# Check whether it is scalr or not. applicaple for both NumberTypes and Arrai
def is_square(object: Arrai):
    if(isinstance(object, Arrai)):
        if(object.shape[0] == object.shape[1]):
            return True
    return False 

def is_scalar(object):
    if(isinstance(object, NumberTypes)):
        return True
    elif(isinstance(object, Arrai)
        and (object.shape[0] is 1) and (object.shape[1] is 1)):
            return True
    
    return False

# Return the scalar in numerical type if it is scalar
def get_scalar(object) -> NumberTypes:
    if(isinstance(object, NumberTypes)):
        return object
    elif(isinstance(object, Arrai) and is_scalar(object)):
        return object[0][0]
    
    return None


if __name__ == "__main__":
    mat = Arrai([[1, 10, 5, 7], [8, 7, 10, 11]])
    mat2 = Arrai([1, 5, 4, 6, 7, 3, 6, 4, 2, 2, -1, 1])
    mat4 = Arrai.arange(8)

    temp = mat.reshape((4, 2))
    temp2 = mat4.reshape((4, 2))

    print(temp)
    print(temp2)
    print(temp+1)


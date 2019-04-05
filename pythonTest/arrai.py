from recursive_functions import *
from enum import Enum

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
                Explosion.INIT_ARGUMENT_TYPE_ERROR.bang();

        self.ndim = 0 # Number of array dimensions.
        self.shape = 0
        self.set_array(object)

    def __repr__(self):
        answer = 'Arrai('
        answer += get_string(self.array, self.ndim - 1, self.ndim, ',', True)
        answer += ')'
        return answer

    def __str__(self):
        answer = ''
        answer += get_string(self.array, self.ndim - 1, self.ndim, ' ', False)
        answer += ''
        return answer

    def __getitem__(self, index):
        return self.array[index]

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
        return ndim;

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


    # overload operator
    def __add__(self, other):
        print(type(other))
        return basic_arithmetic(self, other, '+')

    def __radd__(self, other):
        return self + other;

    def __sub__(self, other):
        return basic_arithmetic(self, other, '-')

    def __rsub__(self, other):
        return basic_arithmetic(self, other, '-')

    def __mul__(self, other):
        return mul(self, other)

    def __rmul__(self, other):
        return mul(self, other)

    def __truediv__(self, other):
        return inv(self, other)

    def row(self, index: int) -> 'Arrai':
        return Arrai(self.array[index])

    def col(self, index: int) -> 'Arrai':
        return Arrai([[self.array[i][index]] for i in range(self.shape[0])])

    def el(self, index: int) -> NumberTypes:
        if(index < shape[0] * shape[1]):
            return self[index / shape[1]][index % shape[1]]


    # Perform element wise arithmetic operation


class Explosion(Enum):
    INIT_ARGUMENT_TYPE_ERROR = TypeError("Argument must be of type list or numerical values(scalar)")
    INVALID_ARRAY_DIM = ValueError('Not a valid n * m array');
    INVALID_NUMERICAL_TYPE = ValueError("Element must be numerical values");
    INVALID_ARITHMETIC_OPERATOR = ValueError("Invalid Operator")
    INVALID_ARITHMETIC_OPERAND = ValueError("Invalid Operand")
    ARITHMETIC_SHAPE_MISMATCH = ValueError("Arithmetic requires both to be of same dimension or either one to be a scalar")
    DOT_SHAPE_MISMATCH = ValueError("Dot requires both to be of same dimension")
    SUM_SHAPE_MISMATCH = ValueError("Sum requires both to be of same dimension")
    DOT_DIM_MISMATCH = ValueError("Array dimension mismatched!")

    def bang(self):
        raise self.value


# helper func for basic arithmetic operation, element-wise
def basic_arithmetic(first: Arrai, second: Arrai, op: str):

    scalar = None

    if(is_scalar(first) or is_scalar(second)):
        (scalar,arr) = (get_scalar(first),second) if is_scalar(first) else (get_scalar(second),first)

    elif (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang();
        return

    if(op == '+'):
        func_op = lambda x, y: x + y
    elif(op == '-'):
        func_op = lambda x, y: x - y
    elif(op == '*'):
        func_op = lambda x, y: x * y
    elif(op == '/'):
        func_op = lambda x, y: x / y
    else:
        Explosion.INVALID_ARITHMETIC_OPERATOR.bang();

    mat = []


    if(scalar is not None):
        if(is_scalar(arr)):
            return Arrai(func_op(scalar, get_scalar(arr)))
        else:
            for i in range(arr.shape[0]):
                row = [];
                for j in range(arr.shape[1]):
                    row.append(func_op(arr[i][j], scalar))
                mat.append(row)
    else:
        if first.shape == second.shape:
            for row1, row2 in zip(first.array, second.array):
                row = [];
                for x, y in zip(row1, row2):

                    row.append(func_op(x,y))
                mat.append(row)
        else:
            Explosion.ARITHMETIC_SHAPE_MISMATCH.bang();


    return Arrai(mat) 



"""
Follow Matlab definition
sum is reserved for python, thus zum is used
dim = 1: summation for all column vectors
dim = 2: summation for all row vectors
"""

def zum(first: Arrai, second: Arrai = None, dim = 1) -> Arrai:
    if(isinstance(second, int)):
        dim = second
        second = None

    if(second == None): 
        second = Arrai.zeros(first.shape)

    if (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang();
        return

    elif(first.shape == second.shape):
        ret = []
        if(dim == 1):
            for i in range(first.shape[1]):
                total = 0
                for j in range(first.shape[0]):
                    total += first[j][i]
                ret.append(total)
        elif(dim == 2):
            for i in first:
                total = 0
                for j in i:
                    total += j
                ret.append([total])
        return Arrai(ret)
    else:
        Explosion.SUM_SHAPE_MISMATCH.bang()



def dot(first: Arrai, second: Arrai, dim = 1) -> Arrai:

    if (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang();
        return

    elif(is_vector(first) and is_vector(second)):
        if(first.shape[0] == 1 and first.shape[1] == second.shape[1]):
            return first * transpose(second)
        elif(first.shape[0] == 1 and first.shape[1] == second.shape[0]):
            return first * second
        elif(first.shape[1] == 1 and first.shape[0] == second.shape[0]):
            return second * transpose(first)
        elif(first.shape[1] == 1 and first.shape[0] == second.shape[1]):
            return  second * first
            
    elif(first.shape == second.shape):
        return zum(basic_arithmetic(first, second, '*'), dim)
    else:
        Explosion.DOT_SHAPE_MISMATCH.bang()



def mul(first: Arrai, second: Arrai) -> Arrai:

    if (is_scalar(first) or is_scalar(second)):
        return basic_arithmetic(first, second, '*')

    elif (isinstance(first, Arrai) and isinstance(second, Arrai)) is False:
        Explosion.INVALID_ARITHMETIC_OPERAND.bang();
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

def inv(first: Arrai, second: Arrai) -> Arrai:
    if (is_scalar(second)):
        return basic_arithmetic(first, second, '/')

    if(not isinstance(first, Arrai)):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()


def transpose(arr: Arrai) -> Arrai:
    ret = [[row[i] for row in arr.array] for i in range(arr.shape[1])]
    return Arrai(ret)

def is_vector(object: Arrai):
    if(isinstance(object, Arrai)):
        if(object.shape[0] == 1 or object.shape[1] == 1):
            return True
    return False

def is_scalar(object):
    if(isinstance(object, NumberTypes)):
        return True
    elif(isinstance(object, Arrai)
        and (object.shape[0] is 1) and (object.shape[1] is 1)):
            return True
    
    return False

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


import copy

from .recursive_functions import *
from .explosion import Explosion
from decimal import Decimal

ERROR = 0.0000000001
NumberTypes = (int, float, complex, Decimal)

class Arrai(object):
    """description of class"""

    # instance methods
    # create an array

    def __init__(self, object: list) -> None:
        # attribute definition
        if (isinstance(object, list) is False
            and isinstance(object, NumberTypes) is False):
                Explosion.INIT_ARGUMENT_TYPE_ERROR.bang()

        if isinstance(object, list) is True and len(object) == 0:
            Explosion.BLANK_ARRAY_PASS_IN.bang()

        self.ndim = 0 # Number of array dimensions.
        self.shape = 0
        self.set_array(object)

    def __repr__(self):
        answer = 'Arrai('
        answer += get_string(self.array, self.ndim - 1, self.ndim, '  ', True)
        answer += ')'
        return answer

    def __str__(self):
        answer = '\n'
        answer += get_string(self.array, self.ndim - 1, self.ndim, '  ', False)
        answer += '\n'

        return answer

    def format_str(self, space : int = 0, prec : int = 4) -> str:
        answer_string = ''
        for row in self.array:
            for el in row:
                if space == 0:
                    answer_string += '{:>.{prec}f}'.format(el, prec=prec)
                else:
                    answer_string += '{:>{space}.{prec}f}'.format(el, space=space, prec=prec)
            answer_string += '\n'
        return answer_string

    def __getitem__(self, index):
        return self.array[index]

    # Operator overloading
    def __add__(self, other):
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
        return reshape(self, shape);

    @classmethod
    def ones(cls, shape: (tuple, list, int)):
        return cls.full(shape, 1)

    @classmethod
    def zeros(cls, shape: (tuple, list, int)):
        return cls.full(shape, 0)

    @classmethod
    def full(cls, shape: (tuple, list), value=0):

        # shape can only contain 2 elements inside
        if len(shape) is not 2:
            # TODO: return exception
            return

        mat = []
        for i in range(shape[0]):
            row = []
            for j in range(shape[1]):
                row.append(value)
            mat.append(row)

        return cls(mat)

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
    def norm(cls, first: list) -> NumberTypes:
        return norm(first[0])

    @classmethod
    def normal(cls, first: list) -> 'Arrai':
        return normalize(first[0])

    @classmethod
    def cross_product(cls, arrais: list) -> 'Arrai':
        return cross_product(arrais[0], arrais[1])

    @classmethod
    def component(cls, arrais: list) -> 'Arrai':
        return component(arrais[0], arrais[1])

    @classmethod
    def projection(cls, arrais: list) -> 'Arrai':
        return projection(arrais[0], arrais[1])

    @classmethod
    def triangle_area(cls, arrais: list) -> NumberTypes:
        return triangle_area(arrais[0], arrais[1])

    @classmethod
    def is_parallel(cls, arrais: list) -> bool:
        return is_parallel(arrais[0], arrais[1])

    @classmethod
    def is_orthogonal(cls, arrais: list) -> bool:
        return is_orthogonal(arrais[0], arrais[1])

    @classmethod
    def angle_degree(cls, arrais: list) -> NumberTypes:
        return angle_degree(arrais[0], arrais[1])

    @classmethod
    def plane_normal(cls, arrais: list) -> 'Arrai':
        return plane_normal(arrais[0], arrais[1])

    @classmethod
    def is_linear_independent(cls, arrais: list) -> bool:
        return is_linear_independent(arrais)

    @classmethod
    def Gram_Schmidt_Orthogonalization(cls, arrais: list) -> 'Arrai':
        return Gram_Schmidt_Orthogonalization(arrais)

    @classmethod
    def rank(cls, first: 'Arrai') -> NumberTypes:
        return rank(first[0])

    @classmethod
    def solve_linear(cls, arrais: list) -> 'Arrai':
        return solve_linsys(arrais[0], arrais[1])

    @classmethod
    def det(cls, arrais: list) -> NumberTypes:
        return det(arrais[0])

    @classmethod
    def inverse(cls, arrais: list) -> 'Arrai':
        return inverse(arrais[0])

    @classmethod
    def adjoint(cls, arrais: list) -> 'Arrai':
        return adjoint(arrais[0])

    @classmethod
    def eigen(cls, arrais: list) -> tuple:
        return eigen(arrais[0])

    @classmethod
    def power_method(cls, arrais: list) -> tuple:
        return power_method(arrais[0])

    @classmethod
    def least_square(cls, arrais: list) -> 'Arrai':
        return least_square(arrais[0], arrais[1])

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

                if(not(isinstance(j, Decimal))):
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
            self.array.append(copy.deepcopy(object))
            self.ndim = 2

        # matrix/ 2D array passing inside
        elif self.ndim == 2:
            self.array = copy.deepcopy(object)

        else:
            
            self.array = None


        if(self.array == None):
            raise ValueError("array cannot be blank")
            #TODO : throw exceptions

        # Transform all elements into type Decimal
        for row in self.array:
            for i in range(len(row)):
                row[i] = Decimal(row[i])

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

    def set_col(self, c: int, vec: 'Arrai') -> 'Arrai':
        return set_col(self, c, vec)

    def swap_row(self, r1: int, r2: int) -> 'Arrai':
        return swap_row(self, r1, r2)

    def swap_col(self, r1: int, r2: int) -> 'Arrai':
        return swap_col(self, r1, r2)

    """
    Return the sub matrix
    r1,r2,c1,c2 are inclusive
    0 <= r1 <= r2 < shape[0], 0 <= c1 <= c2 < shape[1]
    """
    def partition(self, r1: int, r2: int, c1: int, c2: int) -> 'Arrai':
        if not (r1 <= r2 and r2 < self.shape[0]) or not (c1 <= c2 and c2 < self.shape[1]):
            Explosion.INVALID_ARRAY_DIM.boom()
        
        return Arrai([[self.array[i][j] for j in range(c1,c2+1)] for i in range(r1, r2+1)])


from .basic_operations import *
from .basic_arithmetic import *
from .operations import *


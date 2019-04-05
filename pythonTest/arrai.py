from recursive_functions import *

class arrai(object):
    """description of class"""

    # instance methods
    # create an array
    def __init__(self, object: list) -> None:
        # attribute definition
        if (isinstance(object, list) is False
            and isinstance(object, int) is False
            and isinstance(object, float) is False):
                raise TypeError("Argument must be of type list or numerical values")

        self.ndim = 0 # Number of array dimensions.
        self.shape = 0
        self.set_array(object)

    def __repr__(self):
        answer = 'arrai('
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

            return arrai(new_list)

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

    @staticmethod
    def check_validity(self) -> None:
        if(self.ndim != 2):
            return
        for i in self.array:
            if(len(i) != self.shape[1]):
                raise ValueError('Not a valid n * m matrix')
            for j in i:
                if(not(isinstance(j, int) or isinstance(j, float))):
                    raise ValueError("Element must be numerical values")

        return
        # check if this array is a valid array applicable

    def set_array(self, object: list) -> None:

        self.ndim = arrai.get_ndim(object)
        # scalar passing inside, shape will be 1*1
        if self.ndim == 0:
            self.array = [[]]
            self.array[0].append(object)
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
        
        self.shape = arrai.get_shape(self.array)
        arrai.check_validity(self)

    def dot(self, other):
        return dot(self, other);

    def transpose(self):
        return transpose(self);

    def isscalar(self):
        if ((self.shape[0] is 1) and (self.shape[1] is 1)):
            return True
        else:
            return False


    # overload operator
    def __add__(self, other):
        if (isinstance(self, arrai) and isinstance(other, arrai)) is False:
            # TODO: return exception
            return

        temp_list_2S = []
        if self.shape == other.shape:
            for list1, list2 in zip(self.array, other.array):
                temp_list_1S = [];
                for x, y in zip(list1, list2):
                    temp_list_1S.append(x + y)
                temp_list_2S.append(temp_list_1S)

        return arrai(temp_list_2S)

    def __sub__(self, other):
        if (isinstance(self, arrai) and isinstance(other, arrai)) is False:
            # TODO: return exception
            return

        temp_list_2S = []
        if self.shape == other.shape:
            for list1, list2 in zip(self.array, other.array):
                temp_list_1S = [];
                for x, y in zip(list1, list2):
                    temp_list_1S.append(x - y)
                temp_list_2S.append(temp_list_1S)

        return arrai(temp_list_2S)


def dot(a: arrai, b: arrai) -> arrai:
    mat = []
    # only work for vectors ( m*1 / 1*m)
    if (a.shape[0] == b.shape[1] 
        and a.shape[1] == b.shape[0]):

        for i in range(a.shape[0]):
            row = []
            for j in range(b.shape[1]):
                sum_product = 0         
                for k in range(a.shape[1]):
                    sum_product += a.array[i][k] * b.array[k][j]
                row.append(sum_product)
            mat.append(row)
        return arrai(mat)
    else:
        raise ValueError("Array dimension mismatched! (%d * %d) and (%d * %d)" %
            (a.shape[0], a.shape[1], b.shape[0], b.shape[1]))


def transpose(a: arrai) -> arrai:
    ret = [[row[i] for row in a.array] for i in range(a.shape[1])]
    return arrai(ret)


if __name__ == "__main__":
    mat = arrai([[1, 10, 5, 7], [8, 7, 10, 11]])
    mat2 = arrai([1, 5, 4, 6, 7, 3, 6, 4, 2, 2, -1, 1])
    mat4 = arrai.arange(8)

    temp = mat.reshape((4, 2))
    temp2 = mat4.reshape((4, 2))

    print(temp)
    print(temp2)
    print(temp+1)


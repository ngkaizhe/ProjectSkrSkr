from .arrai import *
from .explosion import Explosion
from . import helpers as helpers
import math
from typing import List

""" 
arrai_operation.py

Concrete module for array's operation such as transpose, inverse, arithmetic, etc

"""


def cofactor(arr: Arrai) -> Arrai:
    ret = copy.deepcopy(arr)

    row_count = arr.shape[0]
    col_count = arr.shape[1]

    for i in range(row_count):
        for j in range(col_count):
            mat = []
            for x in range(row_count):
                if(x == i): continue
                row = []
                for y in range(col_count):
                    if(y == j): continue
                    row.append(arr[x][y])
                mat.append(row)

            ret[i][j] = (-1)**(i+j) * det(Arrai(mat))

    return ret

def adjoint(arr: Arrai) -> Arrai:
    return transpose(cofactor(arr))

def transpose(arr: Arrai) -> Arrai:
    return Arrai([[row[i] for row in arr.array] for i in range(arr.shape[1])])

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

# Solve Linear system, whe
def solve_linsys(A: Arrai, B: Arrai) -> Arrai:
    if A.shape[0] != B.shape[0]:
        Explosion.LEAST_SQUARE_ROW_NUM_NOT_EQUAL.bang()
        return

    if is_square(A):
        X = helpers.helper_RREF(A, B)
        return X["B"];
    else:
        return least_square(A, B)

# Least square => x = inv(A'A) * A' * b
def least_square(A: Arrai, B: Arrai) -> Arrai:
    if A.shape[0] != B.shape[0]: # If their row number mismatched
        Explosion.LEAST_SQUARE_ROW_NUM_NOT_EQUAL.bang()
        return

    t_A = transpose(A)
    return inverse(t_A * A) * t_A * B

def null(A: Arrai, flag: str = "") -> Arrai:
    A = helpers.helper_RREF(A)["A"]
    row_count = A.shape[0]
    col_count = A.shape[1]

    no_vars = col_count
    i_unknowns = []

    i_row = 0
    i_col = 0
    while(True):
        if (i_col >= col_count): break
        if (i_row < row_count and not math.isclose(A[i_row][i_col], 0, abs_tol=ERROR)): # If pivot is found, go next row
            i_row += 1
        else:
            i_unknowns.append(i_col) # Keep the index of unknown variables
        i_col += 1


    no_unknowns = len(i_unknowns)
    if (no_unknowns == 0):
        Explosion.NO_NULL_SPACE.bang()
    ans = Arrai.zeros((no_vars, no_unknowns))

    for i in range(no_unknowns):
        ans[i_unknowns[i]][i] = 1
        for j in range(row_count):
            k = j
            while(k < col_count and math.isclose(A[j][k], 0, abs_tol=ERROR)): # Find the pivot in the row
                k += 1
            if(k == col_count): break

            pivot = 0 # value of the pivot variable
            i_pivot = k
            k += 1
            while(k < col_count):
                pivot -= A[j][k] * ans[k][i]
                k += 1
            ans[i_pivot][i] = pivot
            #if(flag != "r"):
             #   ans = ans.set_col(i, normalize(ans.col(i)))
    if (flag != "r"):
        arr = []
        for i in range(ans.shape[1]):
            arr.append(transpose(ans.col(i)))

        ans = transpose(Gram_Schmidt_Orthogonalization(arr))

    return ans

def eigen(A: Arrai) -> (NumberTypes, Arrai):
    if not is_square(A):
        Explosion.EIGEN_NOT_SQUARE.bang()
        return 

    if A.length() == 2:
        a = A[0][0]; b = A[0][1];
        c = A[1][0]; d = A[1][1];

        x = 1
        y = -(a + d)
        z = a*d - b*c

        S = Decimal.sqrt(y**2 - 4*x*z)

        eigen_val = [0,0]
        eigen_val[0] = (-y + S) / (2*x)
        eigen_val[1] = (-y - S) / (2*x)

        eigen_vals = Arrai([[eigen_val[0]],[eigen_val[1]]]);

    elif A.length() == 3:
    # ev^3 + x * ev^2 + y * ev + z

        a = A[0][0]; b = A[0][1]; c = A[0][2]
        d = A[1][0]; e = A[1][1]; f = A[1][2]
        g = A[2][0]; h = A[2][1]; i = A[2][2]

        x = -(a+e+i)
        y = (a*e + a*i + e*i - b*d - c*g - f*h)
        z = a * (f*h - e*i) + b * (d*i - f*g) + c * (e*g - d*h)

        Q = (x**2 - 3*y) / 9
        R = (2*x**3 - 9*x*y + 27*z) / 54

        eigen_val = [0,0,0]
        if(R**2 < Q**3):
            
            theta = math.acos(R / Decimal.sqrt(Q**3))
            S = -2 * Decimal.sqrt(Q)
            T = x / 3
            
            eigen_val[0] = S * Decimal(math.cos(theta/3)) - T
            eigen_val[1] = S * Decimal(math.cos((theta + 2*math.pi)/3)) - T
            eigen_val[2] = S * Decimal(math.cos((theta - 2*math.pi)/3)) - T

            eigen_vectors = Arrai.zeros(A.shape)  
            eigen_vals = Arrai([[eigen_val[0]],[eigen_val[1]],[eigen_val[2]]]);


        else:
            Explosion.POWER_METHOD_ACOS_LARGER_ONE.bang() # acos(a/b), a/b cant be larger than 1

    else:
        Explosion.EIGEN_DIM_NOT_SUPPORTED.bang()

    eigen_vectors = Arrai.zeros(A.shape)  
    for i in range(A.length()):
        
        eigen_vector = null(A - Arrai.identity(A.shape) * eigen_val[i]); # solve for (A - I * lambda) x = 0
        eigen_vectors = eigen_vectors.set_col(i, eigen_vector) # concenate the eigen vectors into matrix

    return (eigen_vectors, eigen_vals)




# This Function find the dorminant eigen values, vectors (normalized)
ERROR_PM = 0.0000001
ITER_LIMIT = 10000
def power_method(A: Arrai) -> (NumberTypes, Arrai):
    
    if not is_square(A):
        Explosion.EIGEN_NOT_SQUARE.bang()
        return 

    x = Arrai.full((A.length(), 1), 1) # Initial guess for x


    approximation  = Arrai.full((A.shape[0], 1), 1)
    prev_approximation = Arrai.zeros((A.shape[0], 1))

    iter_count = 0

    while(iter_count < ITER_LIMIT):
        iter_count += 1
        x = A * x

        max_value = 0
        for i in x: # Attempt to find the max absolute value in x's elements
            if(abs(i[0]) > abs(max_value)): 
                max_value = i[0]

        prev_approximation = approximation;
        approximation = x / max_value # normalize the vector, so that its largest element is 1

        for i in range(A.shape[0]):
            # If there are any of the difference between approximations larger than 0, means havent optimized
            if not math.isclose(approximation[i][0], prev_approximation[i][0], abs_tol=ERROR_PM):
                break
        else:
            break


        # By Rayleigh quotient
        eigen_vector = approximation;
        eigen_value = dot(A * eigen_vector, eigen_vector) / dot(eigen_vector, eigen_vector)
    else:
        Explosion.POWER_METHOD_ITER_OVER_LIMIT.bang("ITER_LIMIT: "+ str(ITER_LIMIT))

    return (normalize(eigen_vector), eigen_value)




"""
Follow Matlab definition
sum is reserved by python for __+__, thus zum is used

For Vector:
return the summed value(scalar) of all element

For Matrix:
dim = 1: summation for all column vectors
dim = 2: summation for all row vectors
"""

def norm(arr: Arrai) -> NumberTypes:
    if not isinstance(arr, Arrai):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(is_vector(arr)):
        return Decimal.sqrt(to_scalar(dot(arr, arr)))
    else:
        Explosion.TYPE_NOT_SUPPORTED.bang("normalization of matrix is not supported")
        # TODO

def normalize(arr: Arrai) -> Arrai:
    if not isinstance(arr, Arrai):
        Explosion.INVALID_ARITHMETIC_OPERAND.bang()
        return

    elif(is_vector(arr)):
        if is_zeros(arr):
            return Arrai.zeros(arr.shape)
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

def cross_product(a: Arrai, b: Arrai) -> Arrai:
    if is_vector(a) and is_vector(b):
        if a.shape[1] == 3 and b.shape[1] == 3:
            temp_vector = []
            a1 = a[0][0]
            a2 = a[0][1]
            a3 = a[0][2]
            b1 = b[0][0]
            b2 = b[0][1]
            b3 = b[0][2]
            temp_vector.append(a2*b3 - a3*b2)
            temp_vector.append(-(a1*b3 - a3*b1))
            temp_vector.append(a1*b2 - a2*b1)
            return Arrai(temp_vector)

        else:
            Explosion.CROSS_PRODUCT_VECTOR_NOT_THREE_DIMENSION.bang()

    else:
        Explosion.CROSS_PRODUCT_NOT_VECTOR.bang()
        return None

def component(a: Arrai, b: Arrai) -> Arrai:
    if is_vector(a) and is_vector(b):
        b = normalize(b)
        return dot(a, b)

    else:
        Explosion.COMPONENT_NOT_VECTOR.bang()
        return None

def projection(a: Arrai, b: Arrai) -> Arrai:
    if is_vector(a) and is_vector(b):
        com = component(a, b)
        b = normalize(b)
        return com * b

    else:
        Explosion.COMPONENT_NOT_VECTOR.bang()
        return None

def triangle_area(a: Arrai, b: Arrai) -> NumberTypes:
    if is_vector(a) and is_vector(b):
        first = a[0]
        second = b[0]

        if len(first) != len(second):
            Explosion.TRIANGLE_AREA_VECTOR_NOT_SAME_DIMENSION.bang()
            return None

        else:
            radians = angle_radians(a, b)
            val_sin = math.sin(radians)

            return Decimal(0.5 * val_sin) * norm(a) * norm(b)

    else:
        Explosion.TRIANGLE_AREA_NOT_VECTOR.bang()
        return None

def angle_degree(a: Arrai, b: Arrai) -> NumberTypes:
    return  math.degrees(angle_radians(a, b))

def angle_radians(a: Arrai, b: Arrai) -> NumberTypes:
    if is_vector(a) and is_vector(b):
        first = a[0]
        second = b[0]

        if len(first) != len(second):
            Explosion.ANGLE_VECTOR_NOT_SAME_DIMENSION.bang()
            return None

        else:
            cos = dot(a, b)[0][0] / (norm(a) * norm(b))
            angle_in_radians = math.acos(cos)

            return angle_in_radians

    else:
        Explosion.ANGLE_NOT_VECTOR.bang()
        return None

def is_parallel(a: Arrai, b: Arrai) -> bool:
    if is_vector(a) and is_vector(b):
        first = a[0]
        second = b[0]

        if len(first) != len(second):
            Explosion.PARALLEL_VECTOR_NOT_SAME_DIMENSION.bang()
            return None

        else:
            if math.isclose(dot(a, b)[0][0], norm(a) * norm(b), abs_tol=ERROR):
                return True

            else:
                return False

    else:
        Explosion.PARALLEL_NOT_VECTOR.bang()
        return None

def is_orthogonal(a: Arrai, b: Arrai) -> bool:
    if is_vector(a) and is_vector(b):
        first = a[0]
        second = b[0]

        if len(first) != len(second):
            Explosion.ORTHOGONAL_VECTOR_NOT_SAME_DIMENSION.bang()
            return None

        else:
            if math.isclose(dot(a, b)[0][0], 0, abs_tol=ERROR):
                return True

            else:
                return False

    else:
        Explosion.ORTHOGONAL_NOT_VECTOR.bang()
        return None

def plane_normal(a: Arrai, b: Arrai) -> Arrai:
    if is_vector(a) and is_vector(b):
        first = a[0]
        second = b[0]

        if len(first) != 3 or len(second) != 3:
            Explosion.PLANE_NORMAL_VECTOR_NOT_THREE_DIMENSION.bang()
            return None

        else:
            return cross_product(a, b)

    else:
        Explosion.PLANE_NORMAL_NOT_VECTOR.bang()
        return None

def is_linear_independent(a: List[Arrai]) -> bool:
    temp = []

    for i in a:
        temp.append(i[0])

    temp = Arrai(temp)

    if rank(temp) == temp.shape[0]:
        return True
    else:
        return False

def Gram_Schmidt_Orthogonalization(a : List[Arrai])-> Arrai:
    u_set = a[:]

    v_set = []
    m = 0
    while m < len(u_set):
        i = 0
        total = u_set[m]

        while i < m:
            total -= projection(u_set[m], v_set[i])
            i += 1

        v_set.append(normalize(total))
        m += 1

    answer = []

    for v in v_set:
        answer.append(v[0])

    return Arrai(answer)


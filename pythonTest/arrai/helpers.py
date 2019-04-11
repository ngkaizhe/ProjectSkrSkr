import copy

from .arrai import *
from .explosion import Explosion
import math
""" 
arrai_helpers.py

This is a module that contains all helpers function inorder to assist complex arrai operations
such as the linear equation solving, finding inverse, calculate determinant, etc

"""


"""
https://rosettacode.org/wiki/Reduced_row_echelon_form for psudocode
Perform element wise arithmetic operation
Reduced Row Echelon Form 
This function performs RREF on arr_A, and if arr_B is supplied,
it'll performs the same row operation as arr_A
A will become I and B will become inverse of A * B
Just like Gaussian Jordan Elimination
"""
def helper_RREF(arr_A: Arrai, arr_B: Arrai = None) -> Arrai: #(tuple(Arrai, Arrai))

    if (not isinstance(arr_A, Arrai) 
        or (arr_B is not None and not isinstance(arr_B, Arrai))):

        Explosion.INVALID_ARGS_NOT_ARRAI.bang()

    i_lead = 0 # Index of column vector in matrix
    row_count = arr_A.shape[0]
    col_count_A = arr_A.shape[1]

    has_B = False

    if arr_B is not None:
        if(arr_B.shape[0] != row_count): # If the row size not matched
            Explosion.RREF_ROWSIZE_MISMATCHED.bang()
            return
        else:
            col_count_B = arr_B.shape[1]
            has_B = True

        ret_B = copy.deepcopy(arr_B)

    ret_A = copy.deepcopy(arr_A)

    rank = 0
    det = Decimal(1.0)

    for r in range(row_count):

        if i_lead >= col_count_A: break # Return when there are all zeros left and no more operation are available

        i = r
        while math.isclose(ret_A[i][i_lead], 0, abs_tol=ERROR): # Search for a non-zero element to swap its row with row r
            i += 1
            if i == row_count: # If it hit the bottom
                i = r # Return to the starting position 
                i_lead += 1 # And move right(in array) by one
                if i_lead == col_count_A: break # Return when there are all zeros left and no more operation are available
        
        if i_lead >= col_count_A: break

        # If it haven't returned yet, means a non-zero lead has been found
        # Swap with the row the non-zero element is

        """
        At below, all swap_row, set_row has been replaced with tranditional method
        swap_row, set_row is much more expensive because they produce a new deep_copy of Arrai every call
        In this case where the mutability is not required, so that modifying it directly is acceptable
        But beware of other case where the mutability is required
        """

        if i != r:
            det *= -1
            # ret_A = swap_row(ret_A, i, r)
            ret_A.array[i], ret_A.array[r] = ret_A.array[r], ret_A.array[i]
            if(has_B): 
                # ret_B = swap_row(ret_B, i, r)
                ret_B.array[i], ret_B.array[r] = ret_B.array[r], ret_B.array[i]

        if not math.isclose(ret_A[r][i_lead], 0, abs_tol=ERROR): # Make the lead to be 1 by dividing whole row by lead itself
            lead = ret_A[r][i_lead]
            det *= lead
            # ret_A = ret_A.set_row(r, ret_A.row(r) / lead);
            ret_A.array[r] = [el / lead for el in ret_A.array[r]]

            if(has_B): 
                # ret_B = ret_B.set_row(r, ret_B.row(r) / lead);
                ret_B.array[r] = [el / lead for el in ret_B.array[r]]


        for i in range(row_count): # Elementary row operation to clean up columns
            if i == r: 
                continue
            lead = ret_A[i][i_lead]
            # ret_A = ret_A.set_row(i, ret_A.row(i) - ret_A.row(r) * lead)
            ret_A.array[i] = [ret_A.array[i][j] - ret_A.array[r][j] * lead for j in range(col_count_A)]
            if has_B: 
                # ret_B = ret_B.set_row(i, ret_B.row(i) - ret_B.row(r) * lead);
                ret_B.array[i] = [ret_B.array[i][j] - ret_B.array[r][j] * lead for j in range(col_count_B)]

        i_lead += 1
        rank += 1 


    ret = dict()
    if(has_B): ret["B"] = ret_B
    ret["A"] = ret_A
    ret["rank"] = rank
    ret["det"] = float(det) if (rank == row_count and is_square(arr_A)) else 0
    return ret






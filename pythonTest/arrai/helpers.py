import copy

from .arrai import *
from .explosion import Explosion
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

    if not isinstance(arr_A, Arrai) or (arr_B is not None and not isinstance(arr_B, Arrai)):
        Explosion.INVALID_ARGS_NOT_ARRAI.bang()

    i_lead = 0 # Index of column vector in matrix
    row_count = arr_A.shape[0]
    col_count = arr_A.shape[1]

    has_B = False

    if(arr_B != None):
        if(arr_B.shape[0] != row_count): # If the row size not matched
            Explosion.RREF_ROWSIZE_MISMATCHED.bang()
            return
        else:
            has_B = True

        ret_B = copy.deepcopy(arr_B)

    ret_A = copy.deepcopy(arr_A)

    rank = 0

    for r in range(row_count):

        if (i_lead >= col_count): break # Return when there are all zeros left and no more operation are available

        i = r
        while (ret_A[i][i_lead] == 0): # Search for a non-zero element to swap its row with row r
            i += 1
            if(i == row_count): # If it hit the bottom
                i = r # Return to the starting position 
                i_lead += 1 # And move right(in array) by one
                if(i_lead == col_count): break # Return when there are all zeros left and no more operation are available
        
        if(i_lead >= col_count): break

        # If it haven't returned yet, means a non-zero lead has been found
        # Swap with the row the non-zero element is
        ret_A = swap_row(ret_A, i, r)
        if(has_B): ret_B = swap_row(ret_B, i, r)


        if(ret_A[r][i_lead] != 0): # Make the lead to be 1 by dividing whole row by lead itself
            lead = ret_A[r][i_lead]
            ret_A = ret_A.set_row(r, ret_A.row(r) / lead);
            if(has_B): ret_B = ret_B.set_row(r, ret_B.row(r) / lead);

        for i in range(row_count): # Elementary row operation to clean up columns
            if(i == r): continue
            lead = ret_A[i][i_lead]
            ret_A = ret_A.set_row(i, ret_A.row(i) - ret_A.row(r) * lead)
            if(has_B): ret_B = ret_B.set_row(i, ret_B.row(i) - ret_B.row(r) * lead);

        i_lead += 1
        rank += 1 

    ret = dict()
    if(has_B): ret["B"] = ret_B
    ret["A"] = ret_A
    ret["rank"] = rank
    return ret



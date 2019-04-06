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
will return a tuple(RREF, INVERSE) if inverse calculation is enabled
otherwise only RREF(of type Arrai) is returned
Just like Gaussian Jordan Elimination
"""
def helper_RREF(arr: Arrai, f_calculate_inverse: bool = False) -> Arrai: #(tuple(Arrai, Arrai))

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
        if(i_lead >= col_count): return ret # Return when there are all zeros left and no more operation are available
        i = r
        while(ret[i][i_lead] == 0): # Search for a non-zero element to swap its row with row r
            i += 1
            if(i == row_count): # If it hit the bottom
                i = r # Return to the starting position 
                i_lead += 1 # And move right(in array) by one
                if(i_lead == col_count): return ret # Return when there are all zeros left and no more operation are available
        
        # If it haven't returned yet, means a non-zero lead has been found
        # Swap with the row the non-zero element is
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
"""
Distances
---------

All the functions here are functions to find the distance between two pieces of data
based on contingency table.

+--------+-----------------+
|        | Row 2           |
+--------+-----+-----+-----+
| Row 1  |     | 1   | 0   |
|        +-----+-----+-----+
|        | 1   | a   | b   |
|        +-----+-----+-----+
|        | 0   | c   | d   |
+--------+-----+-----+-----+

Each function has the same parameters and return values:

Parameters
    a : int
        Count of same 1 numbers.
    b : int
        The sum of 1 in row 1 and 0 in row 2.
    c : int
        Sum 1 in row 2 and 0 in row 1.
    d : int
        Count of same 0 numbers.
    n : int
        Sum of all the numbers.

Returns
    float
        The similarity value between two pieces of data.
"""

from math import sqrt
import warnings

# function to get all the name of the functions
def get_all_functions_name():
    """
    Get all the functions in the module.

    Returns
    -------
    list
        List of functions object.
    """
    funcs = [func for func in globals() if callable(globals()[func])]
    # return excluded list from math and this function
    return funcs[2:]

# get specific function by name
def get_function(name):
    """
    Get function by name.

    Parameters
    ----------
    name : str
        Name of the function.

    Returns
    -------
    function
        Function object.
    """
    return globals()[name]

def hamming(a, b, c, d, n):
    """
    Hamming coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = b+c
        return result
    except:
        return None

def euclidean(a, b, c, d, n):
    """
    Euclidean distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = sqrt(b+c)
        return result
    except:
        return None

def squared_euclidean(a, b, c, d, n):
    """
    Squared Euclidean distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = sqrt((b+c)**2)
        return result
    except:
        return None

def canberra(a, b, c, d, n):
    """
    Canberra distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)**(2/3)
        return result
    except:
        return None

def manhattan(a, b, c, d, n):
    """
    Manhattan distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)
        return result
    except:
        return None

def mean_manhattan(a, b, c, d, n):
    """
    Mean Manhattan distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)/(a+b+c+d)
        return result
    except:
        return None

def cityblock(a, b, c, d, n):
    """
    Cityblock distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)
        return result
    except:
        return None

def minkowski(a, b, c, d, n):
    """
    Minkowski distance from contingency table
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)**1
        return result
    except:
        return None

def vari(a, b, c, d, n):
    """
    Vari distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)/(4*(a+b+c+d))
        return result
    except:
        return None

def size_difference(a, b, c, d, n):
    """
    Size difference from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)**2/((a+b+c+d)**2)
        return result
    except:
        return None

def shape_difference(a, b, c, d, n):
    """
    Shape difference from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (n*(b+c)-((b+c)**2))/((a+b+c+d)**2)
        return result
    except:
        return None

def pattern_difference(a, b, c, d, n):
    """
    Pattern difference from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 4*b*c/((a+b+c+d)**2)
        return result
    except:
        return None

def lance_williams(a, b, c, d, n):
    """
    Lance Williams distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)/(2*a+b+c)
        return result
    except:
        return None

def bray_curtis(a, b, c, d, n):
    """
    Bray-Curtis distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (b+c)/(2*a+b+c)
        return result
    except:
        return None

def hellinger(a, b, c, d, n):
    """
    Hellinger distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*sqrt(1-(a/sqrt((a+b)*(a+c))))
        return result
    except:
        return None

def chord(a, b, c, d, n):
    """
    Chord distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = sqrt(2*(1-(a/sqrt((a+b)*(a+c)))))
        return result
    except:
        return None

def yuleq(a, b, c, d, n):
    """
    Yule-Q distance from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')
    
    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (2*b*c)/(a*d + b*c)
        return result
    except:
        return None
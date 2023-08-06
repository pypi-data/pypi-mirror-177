"""
Similarity
----------

All the functions here are functions to find similarities between two pieces of data
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

from math import log2, sqrt, pi, cos, log10
import numpy as np
import warnings

# function to get all the name of the functions
def get_all_functions_name():
    """
    Get all the functions in the module.

    Returns
    -------
    list
        List of all the functions.
    """
    funcs = [func for func in globals() if callable(globals()[func])]
    # return excluded list from math and this function
    return funcs[6:]

# function to get specific function by name
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

def jaccard(a, b, c, d, n):
    """
    Jaccard coefficient from contingency table.
    """
    
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/(a+b+c)
        return result
    except:
        return None

def dice_2(a, b, c, d, n):
    """
    Dice 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/(2*a+b+c)
        return result
    except:
        return None

def dice_1(a, b, c, d, n):
    """
    Dice 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*a/(2*a+b+c)
        return result
    except:
        return None

def three_way_jaccard(a, b, c, d, n):
    """
    Three-way Jaccard coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 3*a/(3*a+b+c)
        return result
    except:
        return None

def neili(a, b, c, d, n):
    """
    Neili coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*a/((a+b)+(a+c))
        return result
    except:
        return None

def sokal_sneath_1(a, b, c, d, n):
    """
    Sokal-Sneath 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/(a+2*b+2*c)
        return result
    except:
        return None

def sokal_michener(a, b, c, d, n):
    """
    Sokal-Michener coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a+d)/(a+b+c+d)
        return result
    except:
        return None

def sokal_sneath_2(a, b, c, d, n):
    """
    Sokal-Sneath 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*(a+d)/(2*a+b+c+2*d)
        return result
    except:
        return None

def rogers_tanimoto(a, b, c, d, n):
    """
    Rogers-Tanimoto coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a+d)/(a+2*(b+c)+d)
        return result
    except:
        return None

def faith(a, b, c, d, n):
    """
    Faith coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a+0.5*d)/(a+b+c+d)
        return result
    except:
        return None

def gower_legendre(a, b, c, d, n):
    """
    Gower-Legendre coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a+d)/(a+0.5*(b+c)+d)
        return result
    except:
        return None

def intersection(a, b, c, d, n):
    """
    Intersection coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a
        return result
    except:
        return None

def inner_product(a, b, c, d, n):
    """
    Inner product coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a+d
        return result
    except:
        return None

def russell_rao(a, b, c, d, n):
    """
    Russell-Rao coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/(a+b+c+d)
        return result
    except:
        return None

def cosine(a, b, c, d, n):
    """
    Cosine coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/sqrt((a+b)*(a+c))
        return result
    except:
        return None

def gilbert_wells(a, b, c, d, n):
    """
    Gilbert-Wells coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = log2(a) - log2(n) - log2((a+b)/n) - log2((a+c)/n)
        return result
    except:
        return None

def ochiai_1(a, b, c, d, n):
    """
    Ochiai 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/sqrt((a+b)*(a+c))
        return result
    except:
        return None

def forbes_1(a, b, c, d, n):
    """
    Forbes 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = n*a/((a+b)*(a+c))
        return result
    except:
        return None

def fossum(a, b, c, d, n):
    """
    Fossum coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = n*((a-0.5)**2)/((a+b)*(a+c))
        return result
    except:
        return None

def sorgenfrei(a, b, c, d, n):
    """
    Sorgenfrei coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a**2/((a+b)*(a+c))
        return result
    except:
        return None

def mountford(a, b, c, d, n):
    """
    Mountford coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/(0.5*(a*b+a*c)+b*c)
        return result
    except:
        return None

def otsuka(a, b, c, d, n):
    """
    Otsuka coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/sqrt((a+b)*(a+c))
        return result
    except:
        return None

def mc_connaughey(a, b, c, d, n):
    """
    McConnaughey coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a**2-b*c)/((a+b)*(a+c))
        return result
    except:
        return None

def tarwid(a, b, c, d, n):
    """
    Tarwid coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (n*a - (a+b)*(a+c))/(n*a + (a+b)*(a+c))
        return result
    except:
        return None

def kulczynski_2(a, b, c, d, n):
    """
    Kulczynski 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a/2 * (2*a+b+c))/((a+b)*(a+c))
        return result
    except:
        return None

def driver_kroeber(a, b, c, d, n):
    """
    Driver-Kroeber coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a/2)*(1/(a+b) + 1/(a+c))
        return result
    except:
        return None

def johnson(a, b, c, d, n):
    """
    Johnson coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/(a+b) + a/(a+c)
        return result
    except:
        return None

def dennis(a, b, c, d, n):
    """
    Dennis coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a*d - b*c)/sqrt(n*(a+b)*(a+c))
        return result
    except:
        return None

def simpson(a, b, c, d, n):
    """
    Simpson coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/min(a+b, a+c)
        return result
    except:
        return None

def braun_banquet(a, b, c, d, n):
    """
    Braun-Banquet coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a/max(a+b, a+c)
        return result
    except:
        return None

def fager_mcgowan(a, b, c, d, n):
    """
    Fager-McGowan coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a/sqrt((a+b)*(a+c))) - max(a+b, a+c)/2
        return result
    except:
        return None

def forbes_2(a, b, c, d, n):
    """
    Forbes 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (n*a - (a+b)*(a+c))/(n*min(a+b, a+c) - (a+b)*(a+c))
        return result
    except:
        return None

def sokal_sneath_4(a, b, c, d, n):
    """
    Sokal-Sneath 4 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a/(a+b) + a/(a+c) + d/(b+d) + d/(c+d))/4
        return result
    except:
        return None

def gower(a, b, c, d, n):
    """
    Gower coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a+d)/sqrt((a+b)*(a+c)*(b+d)*(c+d))
        return result
    except:
        return None

def pearson_1(a, b, c, d, n):
    """
    Pearson 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (n*(a*d - b*c)**2)/((a+b)*(a+c)*(b+d)*(c+d))
        return result
    except:
        return None

def pearson_2(a, b, c, d, n):
    """
    Pearson 2 coefficient from contingency table.
    """
    x2 = pearson_1(a, b, c, d, n)
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = sqrt(x2/(n + x2))
        return result
    except:
        return None

def pearson_3(a, b, c, d, n):
    """
    Pearson 3 coefficient from contingency table.
    """
    rho = (a*d - b*c)/sqrt((a+b)*(a+c)*(b+d)*(c+d))
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = sqrt(rho/(n + rho))
        return result
    except:
        return None

def pearson_heron_1(a, b, c, d, n):
    """
    Pearson Heron 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a*d - b*c)/sqrt((a+b)*(a+c)*(b+d)*(c+d))
        return result
    except:
        return None

def pearson_heron_2(a, b, c, d, n):
    """
    Pearson Heron 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = cos((pi * sqrt(b*c)/(sqrt(a*d) + sqrt(b*c))))
        return result
    except:
        return None

def sokal_sneath_3(a, b, c, d, n):
    """
    Sokal-Sneath 3 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a+d)/(b+c)
        return result
    except:
        return None

def sokal_sneath_5(a, b, c, d, n):
    """
    Sokal-Sneath 5 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a*d/((a+b)*(a+c)*(b+d)*sqrt(c+d))
        return result
    except:
        return None

def cole(a, b, c, d, n):
    """
    Cole coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = sqrt(2)*(a*d - b*c)/sqrt((a*d - b*c)**2 - (a+b)*(a+c)*(b+d)*(c+d))
        return result
    except:
        return None

def stiles(a, b, c, d, n):
    """
    Stiles coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = log10(n*(abs(a*d - b*c) - n/2)**2 / ((a+b)*(a+c)*(b+d)*(c+d)))
        return result
    except:
        return None

def ochiai_2(a, b, c, d, n):
    """
    Ochiai 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a*d/sqrt((a+b)*(a+c)*(b+d)*(c+d))
        return result
    except:
        return None

def yuleq(a, b, c, d, n):
    """
    Yuleq coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a*d - b*c)/(a*d + b*c)
        return result
    except:
        return None

def yulew(a, b, c, d, n):
    """
    Yulew coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (sqrt(a*d) - sqrt(b*c))/(sqrt(a*d) + sqrt(b*c))
        return result
    except:
        return None

def kulczynski_1(a, b, c, d, n):
    """
    Kulczynski 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a / (b + c)
        return result
    except:
        return None

def tanimoto(a, b, c, d, n):
    """
    Tanimoto coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a / ((a+b) + (a+c) - a)
        return result
    except:
        return None

def disperson(a, b, c, d, n):
    """
    Dispersion coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a*d - b*c)/(a+b+c+d)**2
        return result
    except:
        return None

def hamann(a, b, c, d, n):
    """
    Hamann coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = ((a+d) - (b+c))/(a+b+c+d)
        return result
    except:
        return None

def michael(a, b, c, d, n):
    """
    Michael coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 4*(a*d - b*c)/((a+d)**2 + (b+c)**2)
        return result
    except:
        return None

def goodman_kruskal(a, b, c, d, n):
    """
    Goodman-Kruskal coefficient from contingency table.
    """
    tho = max(a,b) + max(c,d) + max(a,c) + max(b,d)
    tho_diff = max(a+c, b+d) + max(a+b, c+d)
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (tho - tho_diff)/(2*n - tho_diff)
        return result
    except:
        return None

def anderberg(a, b, c, d, n):
    """
    Andersberg coefficient from contingency table.
    """
    tho = max(a,b) + max(c,d) + max(a,c) + max(b,d)
    tho_diff = max(a+c, b+d) + max(a+b, c+d)
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (tho - tho_diff)/(2*n)
        return result
    except:
        return None

def baroni_urbani_buser_1(a, b, c, d, n):
    """
    Baroni-UrbaniBuser 1 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (sqrt(a*d) + a)/(sqrt(a*d) + a + b + c)
        return result
    except:
        return None

def baroni_urbani_buser_2(a, b, c, d, n):
    """
    Baroni-UrbaniBuser 2 coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (sqrt(a*d) + a - (b+c))/(sqrt(a*d) + a + b + c)
        return result
    except:
        return None

def peirce(a, b, c, d, n):
    """
    Peirce coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a*b + b*c)/(a*b + 2*b*c + c*d)
        return result
    except:
        return None

def eyraud(a, b, c, d, n):
    """
    Eyraud coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = n**2 * (n*a - (a+b)*(a+c))/((a+b)*(a+c)*(b+d)*(c+d))
        return result
    except:
        return None

def tarantula(a, b, c, d, n):
    """
    Tarantula coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a*(c+d)/(c*(a+b))
        return result
    except:
        return None

def ample(a, b, c, d, n):
    """
    Ample coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = abs(tarantula(a, b, c, d, n))
        return result
    except:
        return None

def derived_rusell_rao(a, b, c, d, n):
    """
    Derived Rusell-Rao coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = log2(1+a)/log2(1+n)
        return result
    except:
        return None

def derived_jaccard(a, b, c, d, n):
    """
    Derived Jaccard coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = log2(1+a)/log2(1+a+b+c)
        return result
    except:
        return None

def var_of_correlation(a, b, c, d, n):
    """
    Variance of correlation coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (log2(1+a*d) - log2(1+b*c))/log2(1+n**2/4)
        return result
    except:
        return None

def gleason(a, b, c, d, n):
    """
    Gleason coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*a / (2*a+b+c)
        return result
    except:
        return None

def van_der_maarel(a, b, c, d, n):
    """
    Van der Maarel coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (2*a-b-c)/(2*a+b+c)
        return result
    except:
        return None

def consonni_and_todeschini_iv(a, b, c, d, n):
    """
    Consonni and Todeschini (CT IV) coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = np.log(1+a)/np.log(1+a+b+c)
        return result
    except:
        return None

def consonni_and_todeschini_iii(a, b, c, d, n):
    """
    Consonni and Todeschini (CT III) coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = np.log(1+a)/np.log(1+n)
        return result
    except:
        return None

def austin_and_colwell(a, b, c, d, n):
    """
    Austin and Colwell coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (2/np.pi) * (1/np.sin(sqrt((a+d)/n)))
        return result
    except:
        return None

def consonni_and_todeschini_i(a, b, c, d, n):
    """
    Consonni and Todeschini (CT I) coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = np.log(1+a+d)/np.log(1+n)
        return result
    except:
        return None

def phi(a, b, c, d, n):
    """
    Phi coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a*d - b*c)/sqrt((a+b)*(b+d)*(a+c)*(c+d))
        return result
    except:
        return None

def cohen(a, b, c, d, n):
    """
    cohen coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*(a*d - b*c) / sqrt((a+b)*(b+d)+(a+c)*(c+d))
        return result
    except:
        return None

def maxwell_and_pilliner(a, b, c, d, n):
    """
    Maxwell and Pilliner coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = 2*(a*d - b*c) / sqrt((a+b)*(c+d)+(a+c)*(b+d))
        return result
    except:
        return None

def consonni_and_todeschini_v(a, b, c, d, n):
    """
    Consonni and Todeschini (CT V) coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (np.log(1+a*d) - np.log(1+b*c))/np.log(1+(n**2)/4)
        return result
    except:
        return None

def scott(a, b, c, d, n):
    """
    scott coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (4*a*d - (b+c)**2) / ((2*a+b+c)*(2*d+b+c))
        return result
    except:
        return None

def tetrachoric(a, b, c, d, n):
    """
    Tetrachoric coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = np.cos((180)/(1+sqrt((a*d)/(b*c))))
        return result
    except:
        return None

def odds_ratio(a, b, c, d, n):
    """
    odds ratio coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = a*d / (b*c)
        return result
    except:
        return None

def rand(a, b, c, d, n):
    """
    rand coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        N = n*(n-1)/2
        B = a*b + c*d
        C = a*c + b*d
        D = a*d + b*c
        A = N-B-C-D
        result = (A+B)/N
        return result
    except:
        return None

def ARI(a, b, c, d, n):
    """
    ARI coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        N = n*(n-1)/2
        B = a*b + c*d
        C = a*c + b*d
        D = a*d + b*c
        A = N-B-C-D
        result = (abs(N*(A+D) - abs((A+B)*(A+C) + (C+D)*(B+D))))/abs(N**2 - abs((A+B)*(A+C) + (C+D)*(B+D)))
        return result
    except:
        return None

def loevingers_H(a, b, c, d, n):
    """
    loevinger's H coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        p1 = max(a, b) + max(c, d) + max(a, c) + max(b, d)
        p2 = max(a+c, b+d) + max(a+b, c+d)
        result = 1 - (b/(n*p1*p2))
        return result
    except:
        return None

def rogot_and_goldberg(a, b, c, d, n):
    """
    rogot and goldberg coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a/(2*a+b+c)) + d/(2*d+b+c)
        return result
    except:
        return None

def hawkins_and_dotson(a, b, c, d, n):
    """
    hawkins and dotson coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (a/(a+b+c) + d/(b+c+d))/2
        return result
    except:
        return None

def harris_and_lahey(a, b, c, d, n):
    """
    harris and lahey coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (2*(2*d+b+c)/(2*(a+b+c)) + d*(2*a+b+c)/(2*(b+c+d)))
        return result
    except:
        return None

def consonni_and_todeschini_ii(a, b, c, d, n):
    """
    Consonni and Todeschini (CT II) coefficient from contingency table.
    """
    if a < 0 or b < 0 or c < 0 or d < 0 or n < 0:
        raise ValueError('value in confusion matrix cannot less than zero')

    # raise warning if a, b, c, d or n is not integer
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int) or not isinstance(n, int):
        warnings.warn(RuntimeWarning('some value in confusion matrix is not integer'))

    try:
        result = (np.log(1+n) - np.log(1+b+c))/np.log(1+n)
        return result
    except:
        return None
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 14:37:38 2012

@author: bart

"""

from math import exp

def erfcc(x):
    """Complementary error function."""
    
    z = abs(x)
    t = 1. / (1. + 0.5*z)
    r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
        t*(.09678418+t*(-.18628806+t*(.27886807+
        t*(-1.13520398+t*(1.48851587+t*(-.82215223+
        t*.17087277)))))))))
    if (x >= 0.):
        return r
    else:
        return 2. - r

def ncdf(x):
    return 1. - 0.5*erfcc(x/(2**0.5))


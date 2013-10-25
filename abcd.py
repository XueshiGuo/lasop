# -*- coding: utf-8 -*-
"""
Created on Mon Jul 05 18:55:55 2010
Last changed on 

@author: Jonas Neergaard-Nielsen

Tools for calculation of Gaussian beam propagation using ABCD matrix formalism.
All lengths are in units of mm.
"""

import numpy as np
from numpy import pi, conj

# set wavelength to 860 nm
lam = 0.000860

# ====================
# q-parameter formulas
#

def wR2q(w, R):
    """
    q = wR2q(w, R)
    --------------
    Get the q-parameter from a given spot size and radius of curvature.
    """
    return 1/(1/R - 1j * lam / (pi * w**2))
    
def w02q(w0):
    """
    q = w02q(w0)
    ------------
    Get the q-parameter at a waist point from the waist size.
    """
    return 1j * pi * w0**2 / lam

def q2w(q):
    """
    w = q2w(q)
    ----------
    Get the spot size from a given q-parameter.
    """
    return np.sqrt(-lam / (pi * np.imag(1 / q)))

def q2w0(q):
    """
    w0 = q2w0(q)
    ------------
    Get the waist size from a given q-parameter.
    """
    return np.sqrt(np.imag(q) * lam / q)
    
def qABCD(q, M):
    """
    q1 = qABCD(q0, M)
    -----------------
    Transform the q-parameter according to the ABCD matrix M.
    """
    M = np.array(M)
    return (M[0, 0] * q + M[0, 1]) / (M[1, 0] * q + M[1, 1])
    
def qreverse(q):
    """
    q1 = qreverse(q)
    ----------------
    q-parameter transformation when changing propagation direction.
    """
    return -conj(q)
    
def qpropagate(zini, qini, elements, z):
    """
    qout = qpropagate(zini, qini, elements, z)
    ------------------------------------------
    Propagate the q-parameter through an optical system.
    zini, qini : location and value of a known q-parameter of the beam
                 (qini must be given for forward propagation of the beam)
    elements   : list of [z-location, ABCD matrix] descriptions of the 
                 optical elements
    z          : location to calculate output q-parameter (if z < zini, the
                 output q-parameter will still be for forward propagation)
    """
    elements = elements[:]
    elements.sort()
    zt = zini
    qt = qini
    
    if z >= zini:
        elements.reverse()
        while elements:
            el = elements.pop()
            if zt <= el[0] <= z:
                qt += el[0] - zt
                qt = qABCD(qt, el[1])
                zt = el[0]
        qt += z - zt
    else:
        qt = qreverse(qt)
        while elements:
            el = elements.pop()
            if z <= el[0] <= zt:
                qt += zt - el[0]
                qt = qABCD(qt, el[1])
                zt = el[0]
        qt += zt - z
        qt = qreverse(qt)
    
    return qt
        
    
# =============
# ABCD matrices
#

def Mprop(d):
    """
    M = Mprop(d)
    ------------
    ABCD matrix for free space propagation of distance d.
    """
    return np.array([[1, float(d)], [0, 1]])

def Minterface(n0, n1, R='inf'):
    """
    M = Minterface(n0, n1, R='inf')
    ----------------------
    ABCD matrix for the refraction at an interface (with radius of curvature R) 
    from a medium with refractive index n0 to a medium with refractive index n1.
    If no R is given, R=infinite i.e. flat surface is assumed.
    """
    return np.array([[1, 0], [0, float(n0)/float(n1)]])

def Mlens(f):
    """
    M = Mlens(f)
    ------------
    ABCD matrix for a thin lens of focal length f.
    """
    return np.array([[1, 0], [-1/float(f), 1]])
    
def Mmirror(R):
    """
    M = Mmirror(R)
    --------------
    ABCD matrix for a curved mirror with radius of curvature R.
    Concave mirrors have R<0, convex have R>0.
    """
    return np.array([[1, 0], [2/float(R), 1]])


# ########################
# default initializations


#!/usr/bin/python

# Author: Christos Faloutsos
# 
#    Copyright 2013 Christos Faloutsos
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import math
import sys

epsilon = sys.float_info.epsilon # to guard against underflows
minFloat = epsilon
maxFloat = 1.0/epsilon
tol = 0.0001 # tolerance

#
# utility functions - shorthands
#
def LR2P( logRatio ):
    return ( R2P( math.exp( logRatio) ) )

# inverse of above
def P2LR( prob ):
    result = math.log( P2R( prob)  )
    assert( abs( LR2P( result) - prob)  < tol)
    return ( result)

def R2P( ratio ):
    assert ( ratio > 0.0 )
    if( ratio < minFloat):
        return(ratio)
    elif ( ratio * minFloat > 1.0 ):
        return(1.0 - 1.0/ratio)
    else:
        result = ratio / ( 1.0 + ratio) 
        assert ( abs( P2R(result) - ratio) < tol*ratio )
        return ( result)

def P2R( prob):
    assert (prob > 0.0)
    assert (prob < 1.0)
    if( prob < minFloat):
        result = prob
    elif( (1.0 - prob) < minFloat):
        result = maxFloat - 1.0
    else:
        result = prob / (1.0 - prob)
    return( prob / (1.0 - prob) )

#
# the formula, to create the new message m(i,j):
#      m_ratio = blendRatios( 
#                       h_ratio, 
#                       b_ratio(i) / m_ratio(j,i)
#               )
#
def blendRatios(a_r, b_r):
    # epsilon = 0.0001
    assert (abs(a_r + b_r ) > minFloat)
    result = float ( a_r * b_r + 1 ) / float ( a_r + b_r )
    return result

def P2H( prob):
    assert prob>0
    assert prob<1
    return ( prob - 0.5)

def H2P( half_value):
    assert half_value < 0.5
    assert half_value > -0.5
    return (0.5+ half_value)

def myprint(fnum):
    result = "%07.4f" % fnum
    # print result
    return result


#
# mainly for the 'shelve' version
#

def combine(src,dst, NS):
    return NS.join( (src, dst))

def reverse_key(e, NS):
    (src, dst) = split_key(e, NS)
    return combine(dst, src, NS)

def split_key(some_key, NS):
    (src, dst) = some_key.split(NS)
    return (src, dst)


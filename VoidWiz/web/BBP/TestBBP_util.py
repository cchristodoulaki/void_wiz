#!/usr/bin/python

#
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

# harness for the BBP_util.py module
#

import unittest
import BBP_util
import math

class TestBBP_util(unittest.TestCase):
    def setUp(self):
        # self.DG = BBP.DiskGraph("edgefile.csv", 0.3, "phiFile.csv", 0.9)
        self.bla= 3

    def testP2R(self):
        pval = 0.3
        result = BBP_util.R2P( BBP_util.P2R( pval ) )
        self.assertAlmostEqual (\
            result,\
            pval,\
            4,\
            "wrong P2R-R2P:" + str(pval) + " vs " + \
                str(result)
            )

        pval = 0.001
        result = BBP_util.R2P( BBP_util.P2R( pval ) )
        self.assertAlmostEqual (\
            result,\
            pval,\
            4,\
            "wrong P2R-R2P:" + str(pval) + " vs " + \
                str(result)
            )

        rval = 40.0
        p_result = BBP_util.P2R( BBP_util.R2P( rval ) )
        self.assertAlmostEqual (\
            p_result,\
            rval,\
            4,\
            "wrong R2P-P2R:" + str(rval) + " vs " + \
                str(p_result)
            )


    def testLR2P(self):
        p = 0.01
        lr = BBP_util.P2LR(p)
        p_new = BBP_util.LR2P( lr)
        self.assertAlmostEqual( p, p_new, 4, 
            "wrong LR2P: " + str(p) + " vs " + str(p_new) )

        p = 0.5
        lr = BBP_util.P2LR(p)
        p_new = BBP_util.LR2P( lr)
        self.assertAlmostEqual( p, p_new, 4, 
            "wrong LR2P: " + str(p) + " vs " + str(p_new) )

        p = 0.99
        lr = BBP_util.P2LR(p)
        p_new = BBP_util.LR2P( lr)
        self.assertAlmostEqual( p, p_new, 4, 
            "wrong LR2P: " + str(p) + " vs " + str(p_new) )

    def testP2H_2(self):
        p = 0.001
        for p in [0.1, 0.2, 0.5, 0.9]:
            p_new = BBP_util.H2P(  BBP_util.P2H( p ))
            self.assertAlmostEqual (\
                p,\
                p_new,\
                4,\
                "inversion H2P( P2H(p) "+ str(p_new) + " !=  " + str(p)
                )

    def testblendRatios(self):
        a=1.0
        b=1.0
        expectation = 1.0

        result = BBP_util.blendRatios(a, b)
        self.assertAlmostEqual( result, expectation, 4, 
            "wrong blendRatios: blend(" + str(a) + ", " + str(b) + ") = " + 
            str(result) + " != " + str(expectation) )

        a=1.0
        b=5.0
        expectation=1.0
        result = BBP_util.blendRatios(a, b)
        self.assertAlmostEqual( result, expectation, 4, 
            "wrong blendRatios: blend(" + str(a) + ", " + str(b) + ") = " + 
            str(result) + " != " + str(expectation) )

        a = 0.0
        b = 3.5
        expectation= float(1.0/3.5)
        result = BBP_util.blendRatios(a, b)
        self.assertAlmostEqual( result, expectation, 4, 
            "wrong blendRatios: blend(" + str(a) + ", " + str(b) + ") = " + 
            str(result) + " != " + str(expectation) )

        b = 0.0
        a = 3.5
        expectation= float(1.0/3.5)
        result = BBP_util.blendRatios(a, b)
        self.assertAlmostEqual( result, expectation, 4, 
            "wrong blendRatios: blend(" + str(a) + ", " + str(b) + ") = " + 
            str(result) + " != " + str(expectation) )



if __name__ == '__main__':

    verbose = 1
    if(verbose>0):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBBP_util)
        unittest.TextTestRunner(verbosity=4).run(suite)
    else:
        unittest.main()

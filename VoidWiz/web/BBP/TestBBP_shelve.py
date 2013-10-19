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

# harness for the BBP.py module
#

import unittest
import BBP_shelve
import math

class TestBBP_shelve(unittest.TestCase):
    def setUp(self):
        self.SG = BBP_shelve.Shelve_Graph("DATA-DIR/edge-chain6.csv", 0.51, None , 0.9)

    def testChain(self):
        n_iter = 10
        self.SG.run_bp(n_iter)
        results={ 'a':  0.5368,
                  'b': 0.5415,
                  'c' : 0.5438,
                  'd' : 0.5438,
                  'e' : 0.5415,
                  'f' : 0.5368
        }
        for n in results.keys():
            est_val = self.SG.get_belief(n)
            self.assertAlmostEqual (\
                results[n],\
                est_val,\
                4,\
                "wrong Chain6-plain:" + str(est_val) + " vs " + \
                    str( results[n]) + " (node= " + str(n) + " )"
            )

class TestBBP_shelve2(unittest.TestCase):
    def setUp(self):
        self.SG = BBP_shelve.Shelve_Graph("DATA-DIR/edge-chain6.csv", \
        0.51, \
        "DATA-DIR/phi-chain6.csv" , \
        0.9)

    def testChain(self):
        n_iter = 10
        self.SG.run_bp(n_iter)
        results={ 'a':  0.8166436,
                  'b': 0.76501733,
                  'c' : 0.72238517,
                  'd' : 0.68654627,
                  'e' : 0.6556507,
                  'f' : 0.6281035
        }
        for n in results.keys():
            est_val = self.SG.get_belief(n)
            self.assertAlmostEqual (\
                results[n],\
                est_val,\
                4,\
                "wrong Chain6-spike:" + str(est_val) + " vs " + \
                    str( results[n]) + " (node= " + str(n) + " )"
            )

class TestBBP_shelve3(unittest.TestCase):
    def setUp(self):
        self.SG = BBP_shelve.Shelve_Graph("DATA-DIR/edge-chain6.csv", 0.50, None , 0.9)


    def testChain(self):
        n_iter = 10
        self.SG.run_bp(n_iter)
        result=0.5
        for n in self.SG.b_r.keys():
            est_val = self.SG.get_belief(n)
            self.assertAlmostEqual (\
                result,\
                est_val,\
                4,\
                "wrong Chain6-null:" + str(est_val) + " vs " + \
                    str( result) + " (node= " + str(n) + " )"
            )

class TestBBP_shelve4(unittest.TestCase):
    def setUp(self):
        self.SG = BBP_shelve.Shelve_Graph("DATA-DIR/edge-chain6.csv", \
        0.7, \
        None , \
        0.5)


    def testChain(self):
        n_iter = 10
        self.SG.run_bp(n_iter)
        result=0.7
        for n in self.SG.b_r.keys():
            est_val = self.SG.get_belief(n)
            self.assertAlmostEqual (\
                result,\
                est_val,\
                4,\
                "wrong Chain6-noLink:" + str(est_val) + " vs " + \
                    str( result) + " (node= " + str(n) + " )"
            )


if __name__ == '__main__':

    verbose = 1
    if(verbose>0):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBBP_shelve)
        unittest.TextTestRunner(verbosity=4).run(suite)

        suite2 = unittest.TestLoader().loadTestsFromTestCase(TestBBP_shelve2)
        unittest.TextTestRunner(verbosity=4).run(suite2)

        suite3 = unittest.TestLoader().loadTestsFromTestCase(TestBBP_shelve3)
        unittest.TextTestRunner(verbosity=4).run(suite3)

        suite4 = unittest.TestLoader().loadTestsFromTestCase(TestBBP_shelve4)
        unittest.TextTestRunner(verbosity=4).run(suite4)


    else:
        unittest.main()

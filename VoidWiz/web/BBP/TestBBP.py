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
#
# harness for the BBP.py module
#

import unittest
import BBP
import math

class TestBBP(unittest.TestCase):
    def setUp(self):
        self.DG = BBP.DiskGraph("edgefile.csv", 0.3, "phiFile.csv", 0.9)

    def testP2R(self):
        pval = 0.3
        result = BBP.R2P( BBP.P2R( pval ) )
        self.assertAlmostEqual (\
            result,\
            pval,\
            4,\
            "wrong P2R-R2P:" + str(pval) + " vs " + \
                str(result)
            )


if __name__ == '__main__':

    verbose = 1
    if(verbose>0):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBBP)
        unittest.TextTestRunner(verbosity=4).run(suite)
    else:
        unittest.main()

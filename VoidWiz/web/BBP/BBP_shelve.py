#!/usr/bin/python
#
# $Log:$
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
# edits: Christina Christodoulakis


# implement the binary Belief Propagation
# INPUT:
#     edge-file: (src dst) pairs
# OUTPUT:
#     the belief scores for each node 


__version__ = "0.1"

import sys
try:
    import shelve
except ImportError:
    print "ERROR: need shelve module - sudo easy_install shelve"
    sys.exit()
import getopt
# import sqlite3
import os.path
# import fileinput
# import string
import math
import warnings
import csv

# try:
#    import Gnuplot
# except ImportError:
#    print "warning:  won't plot - 'sudo easy_install gnuplot-py' "

try:
    import BBP_util as U
except ImportError:
    print "ERROR: need BBP_util.py from christos"
    sys.exit()

verbose = 0
# plot = 1
# STEP = 5 # for heartbeat
n_iter=10 # default # of iterations of message-passing
phiDefault = 0.48
h_score= 0.9    # homophily score: prob(neighbors are same)
phiFileName=None # file name with exceptions to the phi values
# epsilon = sys.float_info.epsilon # to guard against underflows


class Shelve_Graph:
    """ same specs: 
    Input: (src,dst) pairs
         h (homophily prob)
         and phi probabilities per node
    Output: bp prob per node
    Idea: use a few look-up tables

    Tricky part: we use the ratio transformation P2R():
        For each probability p, we use    p/(1-p)
        because it makes the formulas easier: scalar,
        instead of vectors, for the binary case
    """

    def __init__(self, fname, phiDefault, phiFileName, h_score):
        self.fname = fname
        self.name = fname.strip(".csv")
        self.FS = " "    # field separator
        self.verbose = verbose
        self.phiDefault = phiDefault
        self.default_phi_ratio = U.P2R( self.phiDefault)
        self.default_ratio = 1.0 # 50-50 good vs bad
        self.phiFileName = phiFileName
        if( self.verbose > 0):
            print "\n\tFYI Shelve_Graph class started"
            print "\tFYI self.name= ", self.name
            print "\tFYI self.fname= ", self.fname
            print "\tFYI self.FS= |" + self.FS + "|"
            print "\tFYI self.verbose= ", self.verbose
            print "\tFYI self.phiDefault= ", self.phiDefault
            print "\tFYI self.phiFileName= ", self.phiFileName
        self.h_score = h_score
        self.h_r = U.P2R( self.h_score)
        self.accuracy = 0.0000000001 #  change that, to see more nodes

        # clear all files
        for suffix in [ "_phi_r", "_b_r", "_msgOld_r", "_msgNew_r"]:
            tmp_name = self.name+suffix
            if os.path.isfile( tmp_name):
                self.message( "removing " + tmp_name + " file",1)
                os.remove ( self.name + suffix)
            tmp_name_db = tmp_name + ".db"
            if os.path.isfile( tmp_name_db):
                self.message( "removing " + tmp_name_db + " file",1)
                os.remove ( tmp_name_db )

        self.phi_r = shelve.open( self.name+"_phi_r", writeback = True)
        self.b_r = shelve.open( self.name+"_b_r", writeback = True)
        self.msgOld_r = shelve.open (self.name+"_msgOld_r", writeback = True)
        self.msgNew_r = shelve.open (self.name+"_msgNew_r", writeback = True)

        self.NS="-" # name separator, for edge names: source-dst

        self.parse_edges()
        self.parse_phi()

    def message(self, msg, priority):
        if (priority < self.verbose):
            print "\t"  * (2 + priority) + "FYI " + msg

    def add_edge(self, src, dst):
        key = U.combine(src, dst, self.NS)
        self.msgOld_r[key] = self.default_ratio
        self.msgNew_r[key] = self.default_ratio
    
        self.b_r[src] = self.default_ratio
        self.phi_r[src] = self.default_phi_ratio
        self.b_r[dst] = self.default_ratio
        self.phi_r[dst] = self.default_phi_ratio


    def print_all(self):
        print "\n*** calling print_all"
        for dict in (self.b_r, self.phi_r, self.msgOld_r, self.msgNew_r ):
            print "\n\t dict-name:", str(dict),
            for i in dict.keys():
                print i, " ", "%6.4f" % dict[i]
            print "-------"

    def DBG_print_all_sorted(self):
        fmt1="%7s"
        fmt2="%7.4f"
        # print "\n*** calling print_all_sorted"
        for n in sorted(self.b_r.keys()):
            print fmt1 % n,
        print " | ",
        for e in sorted( self.msgOld_r.keys()) :
            print fmt1 % e,

        if(False):
            print ""
            for n in sorted(self.b_r.keys()):
                print fmt2 % self.b_r[n] ,
            print " | ",
            for e in sorted( self.msgOld_r.keys()) :
                print fmt2 % self.msgOld_r[e] ,
    
            print ""
            for n in sorted(self.b_r.keys()):
                print fmt2 % U.R2P(self.b_r[n]) ,
            print " | ",
            for e in sorted( self.msgOld_r.keys()) :
                print fmt2 % U.R2P(self.msgOld_r[e]) ,
    
        print ""
        for n in sorted(self.b_r.keys()):
            print fmt2 % U.P2H( U.R2P(self.b_r[n])) ,
        print " | ",
        for e in sorted( self.msgOld_r.keys()) :
            print fmt2 % U.P2H( U.R2P(self.msgOld_r[e]) ) ,


        print "\n"

#
# scans the fname file, looking for pairs (src,dst)
# and adds them to the dictionaries/shelves
#
    def parse_edges(self):
        try:
            f = open(self.fname)
        except IOError:
            print "can not open ", self.fname
        for line in f:
            stripped_line = line.strip()
            words = stripped_line.split(self.FS)
            n_items = len(words)
            # if( 2 != n_items):
            #     print "*** WARN: edge file has n = ", n_items,\
            #         " words = ", words
            if( len(stripped_line) == 0 ):
                has_empty_line = True
                # ignore empty lines
            else:
                assert( 2 == n_items)
                src = words[0].strip()
                dst = words[1].strip()
                self.add_edge(src, dst)
                # add the MIRROR edge, too; comment-out, 
                # if this is a directed graph
                self.add_edge(dst, src)
        self.sync_all()


#
# empty caches and synchronize the dictionaries
# This is to improve performance of the 'shelve' functionality
#
    def sync_all(self):
        self.msgOld_r.sync()
        self.msgNew_r.sync()
        self.b_r.sync()
        self.phi_r.sync()

    def close_all(self):
        self.msgOld_r.close()
        self.msgNew_r.close()
        self.b_r.close()
        self.phi_r.close()

    # def empty_all(self):
    #     self.msgOld_r = {}
    #     self.msgNew_r = {}
    #     self.b_r      = {}
    #     self.phi_r    = {}
    #     self.sync_all()

#
# scans the self.phiFile for (node_id, phi_value) pairs
# and adjusts the self.phi_r (prior belief ratios)
#
    def parse_phi(self):
        if( self.phiFileName == None):
            # do nothing - leave the default phi's
            return
        try:
            f = open(self.phiFileName)
        except IOError:
            print "can not open ", self.phiFileName
        # f = open(self.phiFileName)
        self.message("working on phiFile " + self.phiFileName, 1)
        for line in f:
            stripped_line = line.strip()
            words = stripped_line.split(self.FS)
            assert( len(words) == 2 )
            node_id = words[0].strip()
            self.message( "line is " + stripped_line, 0)
            # prob_good = float(words[1].strip())
            prob_good = float(words[1].strip())
            # turn it to ratio, and update the 'shelve'
            self.phi_r[ node_id ] = U.P2R( prob_good )
            self.message("node_id= "+node_id+" prob_good= "+str(prob_good),0)
        self.phi_r.sync()


    def print_beliefs_brief_junk(self):
        delta = 0.001
        print "printing nodes with score outside 0.5 +/- ", delta
        for n in sorted(self.b_r.keys()):
            prob_good = U.R2P( self.b_r[n]  )
            if ( (prob_good < 0.5-delta ) or (prob_good > 0.5 + delta )) :
                print n, U.myprint (prob_good)
        print "----- done ----\n"

#
# returns a list of beliefs, sorted on key
#
    def get_all_beliefs(self):
        result = []
        for n in sorted(self.b_r.keys()):
            value = self.get_belief(n)
            result.append( value )
        return result


    def print_beliefs_brief(self, epsilon=0.00001):
        # tol=0.00001
        tol = epsilon
        print "\n-------- beliefs (brief version) ----"
        for n in sorted(self.b_r.keys()):
            b= self.get_belief(n)
            if( abs(b-0.5) > tol ):
                print "node= ", n, " b= ", b,
                if( b > 0.5):
                    print " POSITIVE"
                else:
                    print ""

    def print_positive_only(self):
        #next line added by cc, web app reads
        # from this and displays the results in the interface, sorted. eventually will do away with this, 
        # output can be read directly (avoid overwriting the same file if multiple ppl using demo)
        bbpwriter = csv.writer(open('bbpresults.csv', 'wb'), delimiter='|', quoting=csv.QUOTE_MINIMAL)
        
        for n in sorted(self.b_r.keys()):
            b= self.get_belief(n)
            if (b > 0.7): 
                phi_of_n = U.R2P(self.phi_r[n])
                print "node= ", n, "\tb= ", "%7.6f" % b,
                print "\t (started with (phi)= ", "%7.6f )" % phi_of_n
                #next line added by cchristodoulaki
                bbpwriter.writerow([n,b])

    def print_beliefs(self):
        print "\n-------- beliefs ----"
        for n in sorted(self.b_r.keys()):
            print "node= ", n, \
                " phi= ",   U.myprint (U.R2P(self.phi_r[n])), \
                " b_r = ",  U.myprint (self.b_r[n]), \
                " b= ",     U.myprint (U.R2P( self.b_r[n] ) ), \
                " b= ", self.get_belief(n)
        print "\n"

    def reset_beliefs(self):
        for n in self.b_r.keys():
            self.b_r[n] = float( math.log( self.phi_r[n] ) )

    def get_belief(self, node_id):
        assert node_id in self.b_r.keys()
        ratio = self.b_r[node_id]
        return U.R2P(ratio)

    def update_beliefs(self):
        self.reset_beliefs() # set to phi's & use their logarithms, temporarily
        for e in self.msgOld_r.keys():
            (src, dst) = U.split_key(e, self.NS)
            # print "** update_beliefs: src= ", src, " dst=", dst
            self.b_r[dst] += math.log( self.msgOld_r[e] )
        for n in self.b_r.keys():
            if( self.b_r[n] > U.maxFloat):
                self.message( "large b_r " + str(self.b_r[n] + " n=" + n ), 0)
            self.b_r[n] = math.exp( self.b_r[n] ) # and now exponentiate back

    def update_messages(self):
        for e in self.msgOld_r.keys():
            (src,dst) = U.split_key(e, self.NS)
            # print "** update_messages: src= ", src, " dst=", dst
            # tricky part - see equations on christos' notebook
            #     in ./DOC/bbp_formulas.tex
            r_e = U.reverse_key(e, self.NS)
            pure_message_r =  self.b_r[src] / self.msgOld_r[r_e]
            self.msgNew_r[e] = U.blendRatios( pure_message_r, self.h_r )
        # update msgOld_r
        for e in self.msgOld_r.keys():
            self.msgOld_r[e] = self.msgNew_r[e]
    
#
# run one step of BP
#
    def one_loop(self):
        old_b_r={}
        for n in self.b_r.keys():
            old_b_r[n] = self.b_r[n]
        self.update_beliefs()
        self.update_messages()

        # check the error of approximation
        max_error_r = 0.0
        error_r = 0.0
        for n in self.b_r.keys():
            error_r = abs( self.b_r[n] - old_b_r[n] )
            # print "\t\t error_r ", error_r, " n= ", n
            max_error_r = max( max_error_r, error_r )
            # print "\t\t max_error_r ", error_r, " n= ", n
        return max_error_r


    def run_bp(self, n):
        # for i in range(n):
        i = 0
        max_error_r = self.accuracy + 1.0 # to force the first loop
        while( i<n and max_error_r > self.accuracy ):
            i += 1
            max_error_r = self.one_loop()

            self.message( "--- after " + str(i) + " iterations ---", -1 )
            # self.message( "max_error_r = "+ str(max_error_r) , 0)
            self.message( "max_error_r = "+ "%g" % max_error_r , -1)
            # self.message( "max_error_r = "+ "%7.6f" % max_error_r , 0)
            if(self.verbose > 1 ):
                self.DBG_print_all_sorted()

        # if max_error_r > self.accuracy:
        #    print "WARNING: did not converge"
        return i, max_error_r

if __name__ == "__main__":
    
    # parse the command line arguments
    def usage():
        print "USAGE: ", sys.argv[0], " [-v] [-h] [-f phi] [-F phiFileName] [-n #steps] edgeFileName "
        print "     [-v --verbose] :	    verbose output"
        print "     [-h --help] :		    help: this very message"
        print "     [-f --phi phiDefault] :        phi Default  "
        print "     [-n --n-iter #iterations] :     #steps  "
        print "     [-F --phiFileName phiFileName] :        phiFileName.csv"
    
    def shiftargs():
        sys.argv[1:] = sys.argv[2:]
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhf:F:H:n:", ["verbose",\
        "help", "phi", "phiFileName", "homophily", "n-iter" ])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    
    # print "initial argv: " , sys.argv
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-v", "--verbose"):
            verbose = verbose + 1
            # print "verbose set to ", verbose
            shiftargs()
        if o in ("-H", "--homophily"):
            h_score =  float(a)
            assert h_score >= 0.0
            assert h_score <= 1.0
            shiftargs()
            shiftargs()
        if o in ("-n", "--n-iter"):
            # assert type(a) is IntType, "n_iter is not an int: %s" % `a`
            n_iter = int(a)
            assert n_iter >  0
            shiftargs()
            shiftargs()
        if o in ("-f", "--phi"):
            phiDefault = float(a)
            assert phiDefault >= 0.0
            assert phiDefault <= 1.0
            shiftargs()
            shiftargs()
        if o in ("-F", "--phiFileName"):
            phiFileName = a
            shiftargs()
            shiftargs()
    
    
    # ...
    if (verbose > 0):
        print "verbose=" , verbose
        print opts
        print "final argv: " , sys.argv
    
    if( len(sys.argv) != 2 ):
        print "ERROR: n arguments = ", len(sys.argv)
        print "ERROR: the argument list: ", sys.argv
        usage()
        sys.exit(-2)
    
    fname = sys.argv[1]

    assert os.path.isfile(fname) ,\
        "Can not find edge file " + fname + " - exiting"
    if( phiFileName == None):
        print "\tFYI: all nodes have default phi", phiDefault
    elif os.path.isfile(phiFileName):
        print "\tFYI:", phiFileName, " found"
    else:
        print "can not find ", phiFileName , " - exiting"
        sys.exit(-3)
    
    if verbose > 0:
        print '\tFYI working on ', fname, ' - DONE'
    
    print "\tFYI: --- starting - loading the edge file"
    SG = Shelve_Graph (fname, phiDefault, phiFileName, h_score)

    if(verbose):
        print "\n --- initial values"
        SG.print_beliefs_brief()

    print "\tFYI: --- starting the iterations --- "

    n = -1
    max_error_r = -1.0
    n, max_error_r = SG.run_bp(n_iter)
    fmt_max_error_r = "%g" % max_error_r
    fmt_accuracy =    "%g" % SG.accuracy

    print "\n --- after ", n, " iterations of ", n_iter, " - max_error_r= ", fmt_max_error_r , " accuracy = ", fmt_accuracy
    if(verbose > 2):
        SG.print_beliefs()
    else:
        # SG.print_beliefs_brief()
        SG.print_positive_only()

    # print "\n --- after ", n_iter, " iterations "
    # SG.print_beliefs_brief()
    # print SG.get_all_beliefs()

    # SG.run_bp(1)
    # print "\n --- after ", n_iter + 1, " iterations "
    # SG.print_beliefs_brief()

    SG.close_all()

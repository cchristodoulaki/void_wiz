#!/usr/bin/python
#
# $Log:$
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

# implement the binary Belief Propagation
# INPUT:
#     edge-file: (src dst) pairs
# OUTPUT:
#     the belief scores for each node 


__version__ = "0.1"

# from Numeric import *
# from LinearAlgebra import *
# from MyGraph import *
# import networkx as NX
# import numpy 
# from cd_lib import *


import getopt
import sys
import sqlite3
import os.path
import fileinput
# import string
import math
from  BBP_util import *

verbose = 0
# plot = 1
# STEP = 5 # for heartbeat
n_iter=10 # default # of iterations of message-passing
phiDefault = 0.48
h_score= 0.9    # homophily score: prob(neighbors are same)
phiFileName=None # file name with exceptions to the phi values



class DiskGraph:
    """ Given a file with (src,dst) pairs
    it treats them as an UNDIRECTED graph
    and computes the BP score for each node
    """

    def __init__(self, fname, phiDefault, phiFileName, h_score):
        self.fname = fname
        self.FS = " "    # field separator
        self.verbose = verbose
        self.phiDefault = phiDefault
        self.phiFileName = phiFileName
        if( self.verbose > 0):
            print "\tFYI self.fname= ", self.fname
            print "\tFYI self.FS= |" + self.FS + "|"
            print "\tFYI self.verbose= ", self.verbose
            print "\tFYI self.phiDefault= ", self.phiDefault
            print "\tFYI self.phiFileName= ", self.phiFileName
        self.h_score = h_score
        # self.b_scores ={} # dictionary, for bp scores
        self.node_set ={}
        self.dbname = None
        self.con = None # db connection
        self.c = None   # db cursor

        self.parseEdges()
        self.parsePhi()

    def close(self):
        self.con.commit()
        self.c.close()
        self.con.close()

    def message(self, msg, priority):
        if (priority < self.verbose):
            print "\t"  * (1 + priority) + "FYI " + msg

#
# parse the file with the prior knowledge (phi's)
# Expects a file with pairs
#   node-id  prob(good)
# and updates the 'nodes' table  accordingly
#
    def parsePhi(self):
        if( self.phiFileName == None):
            # do nothing - leave the default phi's
            return

        try:
            f = open(self.phiFileName)
        except IOError:
            print "can not open ", self.phiFileName
            
        f = open(self.phiFileName)

        self.message("working on phiFile " + self.phiFileName, 1)
        # self.con = sqlite3.connect(self.dbname)
        # self.c = con.cursor()
        assert (self.c != None )
        for line in f:
            words = line.split(self.FS)
            assert( len(words) == 2 )
            node_id = words[0].strip()
            prob_good = float(words[1].strip())
            # lbr = math.log( P2R( prob_good) )
            lbr = P2LR( prob_good)
            self.message("node_id= "+node_id+" prob_good= "+str(prob_good),0)
            assert  self.isNode(node_id), "unknown node "+ str(node_id) 
            self.c.execute('''
                update nodes 
                set priorLogBeliefRatio = ?
                where nodeId = ?
            ''', (lbr, node_id,) )
            # self.execNshow(c,'select * from nodes')

        self.con.commit()
        # c.close()
        # con.close()



#
# returns true, if node_id is a known one
#
    def isNode(self, node_id):
        self.c.execute('''
            select count(nodeId)
            from nodes
            where nodeId = ?
        ''', (node_id,) )
        count = 0
        for row in self.c:
            count += 1
        assert (count == 0 or count == 1)
        # print count
        if (count == 1):
            return True
        elif (count == 0):
            return False

    def parseEdges(self):
        try:
            f = open(self.fname)
        except IOError:
            print "can not open ", self.fname

        self.dbname = self.fname + ".db"
        self.con = sqlite3.connect(self.dbname)
        self.con.create_function("LR2P", 1, LR2P)
        self.c = self.con.cursor()
        assert (self.c != None )
        self.c.execute("""
            create table if not exists edges(
                src,
                dst,
                oldLogMsgRatioForward float,
                oldLogMsgRatioBackward float,
                newLogMsgRatioForward float,
                newLogMsgRatioBackward float,

                primary key(src,dst)
            )
        """)
#xxx
        self.c.execute("""
            create view if not exists edgesNmirrors as
                select * from edges
                union
                select  dst as src, 
                        src as dst ,
                        oldLogMsgRatioBackward as oldLogMsgRatioForward,
                        oldLogMsgRatioForward  as oldLogMsgRatioBackward ,
                        newLogMsgRatioBackward as newLogMsgRatioForward,
                        newLogMsgRatioForward  as newLogMsgRatioBackward 
                from edges
        """)


        # just to be sure, clear the table
        self.c.execute("""
            delete from edges
        """)

        self.c.execute("""
            create table if not exists nodes(
                nodeId PRIMARY KEY,
                priorLogBeliefRatio float,
                oldLogBeliefRatio float, 
                newLogBeliefRatio float 
            )
        """)

        self.c.execute("""
            delete from nodes
        """)

        for line in f:
            words = line.split(self.FS)
            assert( len(words) == 2 )
            src = words[0].strip()
            dst = words[1].strip()
            self.message( "src = " + src + " dst= " + dst , 4)
            self.node_set[src] = 1
            self.node_set[dst] = 1
            # defaultLogRatio = P2LR( defaultPhi )
            defaultLogRatio = 0.0
            dlr = defaultLogRatio
            self.c.execute("""
                insert or replace into edges values (?,?,   ?,?, ?,?)
            """, (src,dst,    dlr, dlr,   dlr, dlr) )
            # phiDefault
            # defaultPhiLogRatio = math.log( P2R( phiDefault ) )
            defaultPhiLogRatio = P2LR( phiDefault )
            dplr = defaultPhiLogRatio
            self.c.execute("""
                insert or replace into nodes values (?,  ?,?,?)
            """, (src,   dplr, dlr, dlr))
            self.c.execute("""
                insert or replace into nodes values (?,  ?,?,?)
            """, (dst,   dplr, dlr, dlr))
        
        f.close()
        self.con.commit()

        if( self.verbose > 1):
            self.execNshow("select * from edges" )
            self.execNshow("""
                select count( * ) from (
                    select distinct src, dst
                    from edges
                )
            """ )
            self.execNshow("select * from edgesNmirrors" )
            self.execNshow("select count(*) from edgesNmirrors" )

        # c.close()
        # con.close()

#
# advance by half step:  gets all messages, and prior belief ('phi')
# and updates the current beliefs
#
# together with 'toc(), they do a full iteration
    def tic(self):
        assert self.c != None, "ERROR: un-initialized cursor in tic()" 

        print "\n******* tic ****"
        self.c.execute("""
            insert or replace into nodes 
            select nodeId, 
                    priorLogBeliefRatio,
                    oldLogBeliefRatio,
                    priorLogBeliefRatio + 
                        sum( edgesNmirrors.oldLogMsgRatioForward)
            from nodes, edgesNmirrors
            where nodes.nodeId = edgesNmirrors.dst
            group by nodeId
        """)
        self.execNshow("select * from nodes")




    def execNshow(self, cmd):
        self.c.execute(cmd)
        print "\n---- executing ---"
        print cmd + "\n"
        for row in self.c:
            print row

    def dbShow(self):
        # con = sqlite3.connect(self.dbname)
        # c = con.cursor()
        self.execNshow("select * from edges")
        self.execNshow("select * from nodes")
        # c.close()
        # con.close()


#
# print each node-id, and the bp  score (probability, (0,1))
#
    def bpResults(self):
        assert( self.c != None )
        # COOL! sql using registered udf LR2P() -> logRatio_to_probability
        self.c.execute(" select nodeId, LR2P( newLogBeliefRatio) from nodes ")
        for row in self.c:
            print "node_id= ", row[0], " bp=", row[1]

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
    if (verbose >= 0):
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
        print phiFileName, " found"
    else:
        print "can not find ", phiFileName , " - exiting"
        sys.exit(-3)
    
    if verbose > 0:
        print '\tFYI working on ', fname, ' - DONE'
    
    DG = DiskGraph(fname, phiDefault, phiFileName, h_score)
    # DG.dbShow()
    DG.bpResults()
    # DG.myprint(3.333333333)
    DG.tic()
    DG.close()

#!/usr/bin/python
# Author: Christina Christodoulakis
# 
#    Copyright 2013 Christina Christodoulakis
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
import sys, getopt
import csv, re, numpy
import itertools

def main(argv):
    inputfile = ''
    outputfile = ''
    linkfile = 'links.csv'
    columns = [0,1,9,24,28]
    tuples = [];
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    
    f = open(inputfile, 'rb')
    spamreader = f.readlines()
    i= 0;
    outfile = open("reducedTrials.csv", 'w+');
    
    for row in spamreader:
        i = i+1;
        attributearray = row.split('::')
        if len(attributearray)==29:
            reducedlist = [attributearray[j] for j in columns]       
        #reducedlist.insert(0, str(i))   
            tuples.append(reducedlist)
            
    tuples.sort();
    dedup = [tuples[i] for i in range(len(tuples)) if i == 0 or tuples[i] != tuples[i-1]]
    
    for row in dedup:
        print row;
        outfile.write("|".join(row));
        
    outfile.close() 
        
#    for t in tuples:
#        print ' '.join(t)  
    tbl2graph(dedup, outputfile, linkfile); 
 


      
def tbl2graph(tbl, out, linkfile):
    #he following dictionaries are all nodes of a diferent type
    ctid_dict = {} # name:id
    countryname_dict = {}
    source_dict = {}
    condition_dict = {}
    drug_dict = {}  
    inc_node_id = 0;
    CTID = 0;
    COUNTRY = 1;
    SOURCE = 2;
    CONDITION = 3;
    DRUG = 4;
    
    #nodes = {}; # key is the node id, value is the information of the node (attribute type and attribute value)
    links = []; # links is a list of [source, target] pairs
    
    nodesjsonArray = "\"nodes\":[";
    linksjsonArray = "\"links\":[";
    csvlinks = "";
    
    # look at each tuple of the table, and for each attribute see if the value already exists in the related dictionary. If the value exists use that id, otherwise insert it to dictionary and use the new id
    for t in tbl:
        #print "t[CTID] = " +t[CTID]
        if t[CTID] in ctid_dict:
            link_src = ctid_dict[t[CTID]];
        else : # this is the first time i see this value for thys attribute type   
            ctid_dict[t[CTID]] = inc_node_id;
            #print "ctid_dict["+t[CTID]+"] = "+ str(inc_node_id)
            link_src = inc_node_id;
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
            nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[CTID]).replace('"', '')+"\" , \"type\":\"CTID\",\"nodeid\":"+str(ctid_dict[t[CTID]])+"},";
        # I have now defined a source
        
        # what is the id for the target country?

    #    if t[COUNTRY] in countryname_dict:
    #        link_trgt = countryname_dict[t[COUNTRY]];
    #    else:     
    #        countryname_dict[t[COUNTRY]] = inc_node_id;
    #        link_trgt = inc_node_id;
    #        inc_node_id=inc_node_id+1; # make a new node id for the next new node
    #        nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[COUNTRY]).replace('"', '')+"\" , \"type\":\"COUNTRY\",\"nodeid\":"+str(countryname_dict[t[COUNTRY]])+"},";
            
    
        # add the country link to the set of links (if it doesnt exist)
    #    link = [link_src,link_trgt]
    #    if link not in links:
    #        links.append(link);
    #        linksjsonArray = linksjsonArray + "{\"source\":"+str(link_src)+",\"target\":"+str(link_trgt)+",\"value\":1, \"age\":\"old\"},";
            
        # what is the id for the target trial source?

        if t[SOURCE] in source_dict:
            link_trgt = source_dict[t[SOURCE]];
        else:     
            source_dict[t[SOURCE]] = inc_node_id;
            link_trgt = inc_node_id;
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
            nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[SOURCE]).replace('"', '')+"\",\"type\":\"SOURCE\",\"nodeid\":"+str(source_dict[t[SOURCE]])+"},";
    
        # add the source link to the set of links (if it doesnt exist)
        link = [link_src,link_trgt]
        if link not in links:
            links.append(link);    
            linksjsonArray = linksjsonArray + "{\"source\":"+str(link_src)+",\"target\":"+str(link_trgt)+",\"value\":1, \"age\":\"old\"},";
        
        # what is the id for the target trial condition?

        if t[CONDITION] in condition_dict:
            link_trgt = condition_dict[t[CONDITION]];
        else:     
            condition_dict[t[CONDITION]] = inc_node_id;
            link_trgt = inc_node_id;
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
            nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[CONDITION]).replace('"', '')+"\",\"type\":\"CONDITION\",\"nodeid\":"+str(condition_dict[t[CONDITION]])+"},";
            
        # add the source link to the set of links (if it doesnt exist)
        link = [link_src,link_trgt]
        if link not in links:
            links.append(link); 
            linksjsonArray = linksjsonArray + "{\"source\":"+str(link_src)+",\"target\":"+str(link_trgt)+",\"value\":1, \"age\":\"old\"},";
            
        # what is the id for the target trial drug?

        if t[DRUG] in drug_dict:
            link_trgt = drug_dict[t[DRUG]];
        else:     
            drug_dict[t[DRUG]] = inc_node_id;
            link_trgt = inc_node_id;
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
            nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[DRUG]).replace('"', '').strip()+"\",\"type\":\"DRUG\",\"nodeid\":"+str(drug_dict[t[DRUG]])+"},";
            
        # add the source link to the set of links (if it doesnt exist)
        link = [link_src,link_trgt]
        if link not in links:
            links.append(link);
            linksjsonArray = linksjsonArray + "{\"source\":"+str(link_src)+",\"target\":"+str(link_trgt)+",\"value\":1, \"age\":\"old\"},";
            csvlinks = csvlinks + str(link_src) +","+str(link_trgt) + "\n"
             
    
    nodesjsonArray = nodesjsonArray[:-1]#remove the last ,
    nodesjsonArray = nodesjsonArray+"]"; 
    linksjsonArray = linksjsonArray[:-1]
    linksjsonArray = linksjsonArray+"]";
    json = "{"+nodesjsonArray+","+linksjsonArray  +"}"           
    outfile = open(out, 'w+');
    outfile.write(json);
    outfile.close();  
    linksfile = open(linkfile, 'w+');
    linksfile.write(csvlinks);
    linksfile.close();
    
    #print "Printing source, target links:"
    #for l in links:
        #print str(l[0]) +","+ str(l[1])
#    print "Printing trial nodes"    
#    printDict(ctid_dict);
#    print "Printing country nodes"
#    printDict(countryname_dict);
#    print "Printing trial source nodes"
#    printDict(source_dict);
#    print "Printing condition nodes"
#    printDict(condition_dict);
#    print "Printing drug nodes"
#    printDict(drug_dict);
      
def printDict(nodeDict):
    print "print node id's with their values"    
    for d in nodeDict:
        print  d + " : " + str(nodeDict[d]);
                
if __name__ == "__main__":
    main(sys.argv[1:])
           
           

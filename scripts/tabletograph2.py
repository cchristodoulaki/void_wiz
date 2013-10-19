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
    linkfile = '../VoidWiz/web/BBP/CanadaCTlinks.csv'
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
    outfile = open("reducedTrialsCanada.csv", 'w+');
    # go through file and filter only columns of interest (as defined in variable columns)    
    for row in spamreader:
        i = i+1;
        attributearray = row.split('::')
        if len(attributearray)==29:
            reducedlist = [attributearray[j] for j in columns]       
            tuples.append(reducedlist)
    # sort the resulting rows        
    tuples.sort();
    # remove duplicate rows
    dedup = [tuples[i] for i in range(len(tuples)) if i == 0 or tuples[i] != tuples[i-1]]

    # write the filtered data to file, delimitered by "|"
    rownum = 0;
    for row in dedup:
        print row;
        outfile.write("\""+str(rownum) +"\"|"+ "|".join(row));
        rownum = rownum +1;
        
    outfile.close() 
        
  
    tbl2graph(dedup, outputfile, linkfile); 

      
def tbl2graph(tbl, out, linkfile):
    #he following dictionaries are all nodes of a different type
    tuple_dict = {} # tuple_:nodeid
    ctid_dict = {} # ctid_:nodeid
    countryname_dict = {} # country_name:id
    source_dict = {} # source_name:id
    condition_dict = {} # condition_name:id
    drug_dict = {}   # drug_name:id
    inc_node_id = 0;
    CTID = 0;
    COUNTRY = 1;
    SOURCE = 2;
    CONDITION = 3;
    DRUG = 4;
    
    #nodes = {}; # key is the node id, value is the information of the node (attribute type and attribute value)
    links = []; # links is a list of [source, target] pairs
    csvgraphlinks = [];
    nodesjsonArray = "\"nodes\":[";
    linksjsonArray = "\"links\":[";
    csvlinks = "";
    tuplecounter=0;
    # for each tuple of the table, 
    # 	for each attribute 
    #	  if the value already exists in the related dictionary. 
    #       use that id, 
    #     else
    #       insert the value to dictionary and use the new id
    for t in tbl:

        tuple_dict[tuplecounter] = inc_node_id;
        link_src = inc_node_id;
	# create a source node
	nodesjsonArray = nodesjsonArray + "{\"name\":\""+str(tuplecounter)+"\" , \"type\":\"tuple_identifier\",\"nodeid\":"+str(inc_node_id)+"},";
	# make a new node id for the next new node        
	inc_node_id=inc_node_id+1; 
	tuplecounter=tuplecounter+1;
	

        if t[CTID] in ctid_dict:
            link_trgt = ctid_dict[t[CTID]];
        else : # this is the first time i see this value for this attribute type   
            ctid_dict[t[CTID]] = inc_node_id;
            link_trgt = inc_node_id;
	    nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[CTID]).replace('"', '')+"\" , \"type\":\"ctid\",\"nodeid\":"+str(inc_node_id)+"},";
	    # make a new node id for the next new node            
	    inc_node_id=inc_node_id+1; 

        # add the new link to the set of links (if it doesnt exist)
        linksjsonArray = add2links(link_src,link_trgt,links, linksjsonArray);  
        csvlinks =  add2graph(link_src,link_trgt,csvgraphlinks, csvlinks);   
       
        # what is the id for the target country?

    #    if t[COUNTRY] in countryname_dict:
    #        link_trgt = countryname_dict[t[COUNTRY]];
    #    else:     
    #        countryname_dict[t[COUNTRY]] = inc_node_id;
    #        link_trgt = inc_node_id;
    #        nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[COUNTRY]).replace('"', '')+"\" , \"type\":\"COUNTRY\",\"nodeid\":"+str(inc_node_id)+"},";
    #        inc_node_id=inc_node_id+1; # make a new node id for the next new node
    
            
    
         # add the new link to the set of links (if it doesnt exist)
         # linksjsonArray = add2links(link_src,link_trgt,links, linksjsonArray);  
         # csvlinks =  add2graph(link_src,link_trgt,csvgraphlinks, csvlinks);
            
        # what is the id for the target trial source?

        if t[SOURCE] in source_dict:
            link_trgt = source_dict[t[SOURCE]];
        else:     
            source_dict[t[SOURCE]] = inc_node_id;
            link_trgt = inc_node_id;

            nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[SOURCE]).replace('"', '')+"\",\"type\":\"source\",\"nodeid\":"+str(inc_node_id)+"},";
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
    
        # add the new link to the set of links (if it doesnt exist)
        linksjsonArray = add2links(link_src,link_trgt,links, linksjsonArray);  
        csvlinks =  add2graph(link_src,link_trgt,csvgraphlinks, csvlinks); 
        
        # what is the id for the target trial condition?

        if t[CONDITION] in condition_dict:
            link_trgt = condition_dict[t[CONDITION]];
        else:     
            condition_dict[t[CONDITION]] = inc_node_id;
            link_trgt = inc_node_id;
            nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[CONDITION]).replace('"', '')+"\",\"type\":\"medcondition\",\"nodeid\":"+str(inc_node_id)+"},";
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
            
        # add the new link to the set of links (if it doesnt exist)
        linksjsonArray = add2links(link_src,link_trgt,links, linksjsonArray);  
        csvlinks =  add2graph(link_src,link_trgt,csvgraphlinks, csvlinks); 
            
        # what is the id for the target trial drug?

        if t[DRUG] in drug_dict:
            link_trgt = drug_dict[t[DRUG]];
        else:     
            drug_dict[t[DRUG]] = inc_node_id;
            link_trgt = inc_node_id;
	    nodesjsonArray = nodesjsonArray + "{\"name\":\""+(t[DRUG]).replace('"', '').strip()+"\",\"type\":\"drug\",\"nodeid\":"+str(inc_node_id)+"},";
            inc_node_id=inc_node_id+1; # make a new node id for the next new node
            
            
        # add the new link to the set of links (if it doesnt exist)
        linksjsonArray = add2links(link_src,link_trgt,links, linksjsonArray);  
        csvlinks =  add2graph(link_src,link_trgt,csvgraphlinks, csvlinks);     
             
    
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
    

#    print "Printing trial nodes"    
#    printDict(ctid_dict);

# for json file
def add2links(link_src,link_trgt,links,linksjsonArray):    
    # add the new link to the set of links (if it doesnt exist)
    link = [link_src,link_trgt]
    if link not in links:
    	links.append(link);    
        return linksjsonArray + "{\"source\":"+str(link_src)+",\"target\":"+str(link_trgt)+",\"value\":1, \"age\":\"old\"},";

# for csv file          
def add2graph(link_src,link_trgt,csvgraphlinks,csvlinks):
    # add the new link to the set of links (if it doesnt exist)
    link = [link_src,link_trgt]
    if link not in csvgraphlinks:
    	csvgraphlinks.append(link); 
	return csvlinks + str(link_src) +" "+str(link_trgt) + "\n";   
   
def printDict(nodeDict):
    print "print node id's with their values"    
    for d in nodeDict:
        print  d + " : " + str(nodeDict[d]);
                
if __name__ == "__main__":
    main(sys.argv[1:])
           
           

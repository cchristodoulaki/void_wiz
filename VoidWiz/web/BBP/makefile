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

SRC= 	BBP.py TestBBP.py  \
	BBP_util.py TestBBP_util.py \
	BBP_shelve.py TestBBP_shelve.py

INP= edgefile.csv phiFile.csv
OTHER= README.txt makefile DOC/*.tex DOC/*.lyx DOC/makefile
ALL= $(SRC) $(INP) $(OTHER)
PYTHON= python

demo_shelve:
	$(PYTHON) BBP_shelve.py -v -v \
	    -f 0.314 \
	    -F phiFile.csv \
	    -H 0.8345 \
	    -n 4 \
	    edgefile.csv

demo4: BBP.py edgefile.csv
	$(PYTHON) BBP.py -v -v -v -v edgefile.csv

demo1: BBP.py edgefile.csv
	$(PYTHON) BBP.py -v    -f 0.3 -F phiFile.csv -H 0.9 -n 10 edgefile.csv

demo2: BBP.py edgefile.csv
	$(PYTHON) BBP.py -v -v -f 0.3 -F phiFile.csv -H 0.9 -n 10 edgefile.csv

demo: BBP.py edgefile.csv phiFile.csv
	$(PYTHON) BBP.py -f 0.4 -F phiFile.csv -H 0.67 -n 10 edgefile.csv

### christina c added this ############################################################
cc: BBP_shelve.py patientVisit.csv phiPat.csv                                         
	$(PYTHON) BBP_shelve.py -f 0.49 -F phiPat.csv -H 0.9 -n 20 patientVisit.csv   
	
ccCT: BBP_shelve.py CanadaCTlinks.csv PhiCT.csv                                         
	$(PYTHON) BBP_shelve.py -f 0.6 -F PhiCT.csv -H 0.4 -n 50 CanadaCTlinks.csv        
#######################################################################################

dbshow: edgefile.csv.db
	sqlite3 edgefile.csv.db 'select * from nodes'


spotless: clean
	\rm -rf TST *.pyc
	\cd DOC; make spotless




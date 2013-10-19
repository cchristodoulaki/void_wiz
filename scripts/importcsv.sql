LOAD DATA LOCAL INFILE '/Users/christina/millerSVN/christinashared/scripts/reducedTrials.csv' 
INTO TABLE hospital.clinicalTrial FIELDS TERMINATED BY '|' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n';

# This script takes large output files from Datastage
# and splits them into multiple individual .dsx files
# (usually for purposes of source control.) The 
# input/output folders are expected in directory where
# this file exists. Place your large .dsx files in the 
# input directory and run the script. Output directory
# will contain individual .dsx items contained within 
# those large .dsx files. Only DSJOB and DSTABLEDEFS
# are supported by this script at the moment.
import os
import glob
import re

# begin/end patterns to match
bp = re.compile('BEGIN (DSJOB|DSTABLEDEFS)')
ep = re.compile('END (DSJOB|DSTABLEDEFS)')

# function to create directory if it doesn't exist
def createDirIfNotExists( str ):
	if not os.path.exists(str):
		os.makedirs(str)
	return
	
# function to return name of Identifier
def getIdentifier( str ):
	for line in str.split("\n"):
		if "Identifier" in line:
			ln = line.strip()
			break
	ret = line[line.find('"')+1:line.rfind('"')]
	# check for periods with reverse find to handle table names
	# if period present, take substring from first rfind to end
	if ret.rfind('.') > 0:
		return ret[ret.rfind('.')+1:len(ret)]
	else:
		return ret

# Change directory into input to process files
os.chdir('input')

# for each file in the input directory, do this...
for infile in glob.glob( '*.dsx'):
	print('Processing file : ' + infile)
		
	# get file name (for creating directory)
	s = infile.find('.')
	fn = infile[0:s]
	print('Creating directory if it doesn\'t exist in output : ' + fn)
	createDirIfNotExists( '../output/' + fn )
	
	# open current file, assign variable to content within
	f = open(infile,'r')
	fc = f.read()
	
	# get start/end ordinals for substringing out the ds job/table/etc
	print('Getting matches on begin/end patterns, assigning blocks')
	starts = [match.start() for match in re.finditer(bp,fc)]
	ends = [match.end() for match in re.finditer(ep,fc)]
	
	# iterate through matches and get substring
	for i in range(0,len(starts)):
		print('Getting block from match ordinals')
		block = fc[starts[i]:ends[i]]
		# Get name for new file to be created by passing block to function 
		dsx = getIdentifier( block )
		# Create new file in directory created above
		print('Creating new file: ' + dsx + '.dsx in ' + '../output/' + fn)
		nf = open('../output/' + fn + '/' + dsx + '.dsx', 'w')
		nf.write(block)
		nf.close()

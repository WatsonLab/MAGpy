#!/usr/bin/env python

# Import the module
import subprocess
import sys
import os
import errno

if len(sys.argv) == 1:
	print("Please provide a filename")
	sys.exit()

# output file
outfile = sys.argv[1]

if not os.path.dirname(outfile) == '':
	if not os.path.exists(os.path.dirname(outfile)):
		try:
			os.makedirs(os.path.dirname(outfile))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

f = open(outfile, 'w+')

# try to run checkM
try:
	p1 = subprocess.Popen(['pfam_scan.pl', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# Run the command
	allout = p1.communicate()
	output = allout[0]
	error  = allout[1]
except OSError as o:
	f.write('OSError: is pfam_scan.pl installed and in your PATH?' + '\n')
	f.close()
	sys.exit()
except:
	f.write('Unexpected error: unable to run pfam_scan.pl' + '\n')
	f.close()
	sys.exit()

teststr = error.decode(sys.stdout.encoding)

# if we're still here, check error and print
if teststr[1:29] == 'pfam_scan.pl: search a FASTA':
	f.write('pfam_scan.pl ran without problems' + '\n')
else :
	f.write('pfam_scan.pl ran with some errors: ' + error.decode(sys.stdout.encoding) + '\n')
	
f.close()



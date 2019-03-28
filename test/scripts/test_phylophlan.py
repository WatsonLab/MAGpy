#!/usr/bin/env python

# Import the module
import subprocess
import sys
import os
import errno

if len(sys.argv) == 1:
	print("Please provide a filename")
	sys.exit()

# phylophlan dir
phydir = sys.argv[1]

if not os.path.exists(phydir) or not os.path.isdir(phydir):
	print(phydir + " does not exist or isn't a directory")
	sys.exit()	

# output file
outfile = sys.argv[2]

if not os.path.dirname(outfile) == '':
	if not os.path.exists(os.path.dirname(outfile)):
		try:
			os.makedirs(os.path.dirname(outfile))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

f = open(outfile, 'w+')

# try to run usearch
try:
        p1 = subprocess.Popen(['usearch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Run the command
        usearch = p1.communicate()
        output = usearch[0]
        error  = usearch[1]
except OSError as o:
        f.write('OSError: make sure usearch is installed properly' + '\n')
        f.close()
        sys.exit()
except:
        f.write('Unexpected error: unable to run usearch' + '\n')
        f.close()
        sys.exit()

# if we're still here, check error and print
if error == '':
        f.write('usearch ran without problems' + '\n')
else :
        f.write('usearch ran with some errors: ' + error + '\n')



# try to run phylophlan
try:
	os.chdir(phydir)
	p1 = subprocess.Popen(['./phylophlan.py','-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# Run the command
	checkm = p1.communicate()
	output = checkm[0]
	error  = checkm[1]
except OSError as o:
	f.write('OSError: make sure phylophlan is installed properly' + '\n')
	f.close()
	sys.exit()
except:
    f.write('Unexpected error: unable to run phylophlan' + '\n')
    f.close()
    sys.exit()

# if we're still here, check error and print
if error == '':
	f.write('phylophlan ran without problems' + '\n')
else :
	f.write('phylophlan ran with some errors: ' + error + '\n')
	

f.close()



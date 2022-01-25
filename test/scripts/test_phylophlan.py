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

# try to run phylophlan
try:
    p1 = subprocess.Popen(['phylophlan','-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Run the command
    checkm = p1.communicate()
    output = str(checkm[0])
    error  = str(checkm[1])

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
else:
    f.write('phylophlan ran with some errors: ' + str(error) + '\n')
	
f.close()

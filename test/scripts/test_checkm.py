#!/usr/bin/env python

# Import the module
import subprocess
import sys
import os
import errno

if len(sys.argv) == 1:
    print "Please provide a filename"
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
    p1 = subprocess.Popen(['checkm'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Run the command
    checkm = p1.communicate()
    output = checkm[0]
    error  = checkm[1]
except OSError as o:
    f.write('OSError: make sure checkM is installed properly' + '\n')
    f.close()
    sys.exit()
except:
    f.write('Unexpected error: unable to run checkM' + '\n')
    f.close()
    sys.exit()

# if we're still here, check error and print
if error == '':
    f.write('CheckM ran without problems' + '\n')
else:
    f.write('CheckM ran with some errors: ' + error + '\n')

f.close()

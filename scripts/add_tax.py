#!/usr/bin/env python

import sys

from ete3 import NCBITaxa

# get NCBI taxonomy object
ncbi = NCBITaxa()

if len(sys.argv) == 1:
    print("Please provide a filename")
    sys.exit()

# open the file
checkm_file = open(sys.argv[1], mode="r")

# skip three lines
row1 = checkm_file.readline()
row2 = checkm_file.readline()
row3 = checkm_file.readline()

# print titles for the output
titles = [
    "bin_id",
    "marker_lineage",
    "ml_uid",
    "n_genomes",
    "n_markers",
    "n_marker_sets",
    "n_0",
    "n_1",
    "n_2",
    "n_3",
    "n_4",
    "n_5_plus",
    "completeness",
    "contamination",
    "strain_het",
    "superkingdom",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus"
]

print('\t'.join(map(str, titles)))

# iterate over file
for row in checkm_file:
    # split on whitespace
    arr = row.split()

    # only consider data lines
    if len(arr) > 1:
        # get taxonomy free of the k__ bit	
        if arr[1] == "root":
            tax = "root"
        else:
            tax = arr[1].split("__")[1]

        # map taxid and tax names
        name2taxid = ncbi.get_name_translator([tax])

        # empty variables unless we change them
        sk = ''
        k  = ''
        p  = ''
        c  = ''
        o  = ''
        f  = ''
        g  = ''

        # check we got what we asked for
        if tax in name2taxid.keys():
            # we want the taxonomy ID
            taxid = name2taxid[tax]

            # get entire lineage from this tax id
            lineage = ncbi.get_lineage(taxid[0])

            # get all names for that lineage
            names = ncbi.get_taxid_translator(lineage)

            # iterate up the lineage mapping names
            # to each of our variables
            for l in lineage:
                rank = ncbi.get_rank([l])

                if rank[l] == 'superkingdom':
                    sk = names[l]

                if rank[l] == 'kingdom':
                    k = names[l]

                if rank[l] == 'phylum':
                    p = names[l]

                if rank[l] == 'class':
                    c = names[l]

                if rank[l] == 'order':
                    o = names[l]

                if rank[l] == 'family':
                    f = names[l]

                if rank[l] == 'genus':
                    g = names[l]	

        # print it all out
        print('\t'.join(map(str, arr)), '\t', end='')
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sk, k, p, c, o, f, g))

# close file
checkm_file.close()

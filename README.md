# MAGpy
MAGpy is a Snakemake pipeline for downstream analysis of metagenome-assembled genomes (MAGs) (pronounced **mag-pie**)

## Citation

Robert Stewart, Marc Auffret, Tim Snelling, Rainer Roehe, Mick Watson (2018) MAGpy: a reproducible pipeline for the downstream analysis of metagenome-assembled genomes (MAGs). Bioinformatics bty905, [bty905](https://doi.org/10.1093/bioinformatics/bty905)

## How to install

Follow the "10 minute install" [here](https://github.com/WatsonLab/MAGpy/blob/master/install.md)

## Clean your MAGs

There are a few things you will need to do before you run MAGpy, and these are due to limitations imposed by the software MAGpy runs, rather than by MAGpy itself.  

These are:

* the names of contigs in your MAGs must be globally unique.  Some assemblers, e.g. Megahit, output very generic contig names e.g. "scaffold_22" which, if you have assembled multiple samples, may be duplicated in your MAGs.  This is not allowed.  BioPython and/or BioPerl can help you rename your contigs
* The MAG FASTA files must start with a letter
* The MAG FASTA files should not have any "." characters in them, other than the final . before the file extension e.f. mag1.faa is fine, mag.1.faa is not

## Reproducibility

For workflows to be reproducible, we recommend that whilst following the ["10 minute install"](https://github.com/WatsonLab/MAGpy/blob/master/install.md) that you name the downloaded databases with the database version and/or the database download date.

if you do this, then the name of the database will be propagated throughout all of the Snakemake outputs and will therefore provide an exact record of what was done, by what software and on which version of the database (software versions are controlled/recorded by the yaml files in the envs directory)

Doing this will ensure reproducibility accross different platforms and groups.

## Run the tests!

It's always a good idea to run the tests and this has the added advantage of installing all of the conda environments.

Clone the repo:

```sh
git clone https://github.com/WatsonLab/MAGpy.git
cd MAGpy
```

Run the tests:

```sh
snakemake --use-conda -s MAGpy --cores 1 test
```

Test outputs will be in ```test/outputs``` and you should have an ```error_log``` file in your current working directory.

## How to run

MAGpy is slightly different to other software tools that you may install.  Rathen than installing MAGpy once, in e.g. a global software directory, it is better to clone the repo each time you wish to use it.  Therefore for each project you wish to run MAGpy on, simply clone the repo into that project's folder, and run MAGpy from there.  New project?  Clone the repo again.  The disk footprint of MAGpy is tiny so you lose nothing by doing this (and conda should handle the multiple environments fine).

Clone the repo:

```sh
git clone https://github.com/WatsonLab/MAGpy.git
cd MAGpy
```

Edit the config.json and point to the databases and directories created during the ["10 minute install"](https://github.com/WatsonLab/MAGpy/blob/master/install.md)

In this directory, put all of your genomes into the mags folder, one file per genome, with a .fa file extension

Then to run in basic (linear, non-cluster) mode, where `$N` is the number of parallel threads you want to use:

```
snakemake --use-conda -s MAGpy --cores $N
```

Outputs will be placed into the *current working directory*, so make sure you have write access.

To test which commands snakemake will run, you can try:

```sh
snakemake -np -s MAGpy
```

However, on any serious number of MAGs, this basic operation will take a very long time as each job will be run in serial (i.e. one after the other).  However, snakemake has the ability to submit to most HPC clusters.  There are some instructions [here](http://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#cluster-execution).  

Here at Edinbugh, we run an SGE cluster and this is how we run MAGpy on the cluster:

```sh
snakemake --use-conda --cluster-config MAGpy.json --cluster "qsub -V -cwd -pe sharedmem {cluster.core} -l h_rt= {cluster.time} -l h_vmem={cluster.vmem} -P {cluster.proj}" --jobs 1000
```

This mode looks into the MAGpy.json file for cluster configurations relating to each type of job; the jobs are "rules" within the MAGpy snakefile.


## The integration of PhyloPhlAn

OK, this is a bit complex.  Essentially, PhyloPhlAn has a few foibles, which are:

* input to PhyloPhlAn **has to be** placed in the ```input/``` directory contains within the PhyloPhlAn install directory
* output from PhyloPhlAn is written to the ```output/``` directory within the PhyloPhlAn install directory
* The PhyloPhlAn process **has to be run** from the root of the PhyloPhlAn install directory

Therefore, whatever user is running the MAGpy process, whether it be on a cluster or a single machine, must have read and write access to the ```input/``` and ```output/``` directories in the PhyloPhlAn install directory

Here is what MAGpy attempts to do:

* It copies protein files into the input directory of PhyloPhlAn
* It then attempts to ```cd``` into the PhyloPhlAn install directory
* From there, it runs PhyloPhlAn
* When finished, it attempts to ```mv``` the results folder back to the original directory (to folder ```tree```)
* MAGpy then changes back to the original working directory

Now obviously this is a bit, erm, hacky but as long as permissions are set on the PhyloPhlAn directory correctly, it should work.

## Drawing the tree

The way we have snakemake set up, it is in a Python 3.5 env and GraPhlAn is in a Python 2.7 env.  So we create the tree outside of Snakemake:

```
conda env create -f envs/basic2.yaml
source activate basic2

perl scripts/produce_tree.pl checkm_plus.txt tree/folder/path_to_newick.nwk
```



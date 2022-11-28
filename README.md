# MAGpy
MAGpy is a Snakemake pipeline for downstream analysis of metagenome-assembled genomes (MAGs) (pronounced **mag-pie**)

## Citation

Robert Stewart, Marc Auffret, Tim Snelling, Rainer Roehe, Mick Watson (2018) MAGpy: a reproducible pipeline for the downstream analysis of metagenome-assembled genomes (MAGs). Bioinformatics bty905, [bty905](https://doi.org/10.1093/bioinformatics/bty905)

## Clean your MAGs

There are a few things you will need to do before you run MAGpy, and these are due to limitations imposed by the software MAGpy runs, rather than by MAGpy itself.  

These are:

* the names of contigs in your MAGs must be globally unique.  Some assemblers, e.g. Megahit, output very generic contig names e.g. "scaffold_22" which, if you have assembled multiple samples, may be duplicated in your MAGs.  This is not allowed.  BioPython and/or BioPerl can help you rename your contigs
* The MAG FASTA files must start with a letter
* The MAG FASTA files should not have any "." characters in them, other than the final . before the file extension e.f. mag1.faa is fine, mag.1.faa is not

## NEW RELEASE - June 2021

* updated to Sourmash 4.1.1
* updated to PhyloPhlAn 3.0.2
* updated to DIAMOND 2.0.9

## Install conda

Skip if you already have it. Instructions are [here](https://docs.conda.io/en/latest/miniconda.html)

## Clone the repo

```
git clone https://github.com/WatsonLab/MAGpy.git
cd MAGpy
```

## Install Snakemake and mamba

Skip if you already have them

```sh
conda env create -f envs/install.yaml 
```

## Run tests and install conda envs:

```
snakemake -rp -s MAGpy --cores 1 --use-conda test
```

## Build the databases

This will build a DIAMOND database of the whole of UniProt TREMBL, so you will need to give it a lot of resources (RAM) - try 256Gb.

```
rm -rf magpy_dbs
snakemake -rp -s MAGpy --cores 16 --use-conda setup
```

## Run MAGpy

```
snakemake -rp -s MAGpy --use-conda --cores 8
```

For large workflows, I recommend you use [cluster](https://snakemake.readthedocs.io/en/stable/executing/cluster.html) or [cloud](https://snakemake.readthedocs.io/en/stable/executing/cloud.html) execution.

Also, for any large number of MAGs, PhyloPhlAn will take a long time - e.g. a few weeks for a couple of thousand MAGs.


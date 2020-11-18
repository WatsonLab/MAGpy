# 10 minute install

(not taking into account downloading and building the databases)

## Assuming we are in a brand new Ubuntu instance

### 1 Update ubuntu
```sh
sudo apt-get update
sudo apt install gcc g++ make wget git
```

### 2 install usearch 

Make sure you download VERSION 5.2.32!

I can't do anything else to help you here - you need to register and you will be sent a link by email.

[link](https://www.drive5.com/usearch/download.html)

Make sure the executable is in your PATH

### 3 download and install conda

(note if you already have a working, functioning install of conda, this step may be unnecessary)

```sh
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# install it
sh Miniconda3-latest-Linux-x86_64.sh

# review license
# accept license
# accept or change home location
# yes to running conda init to place it in your path

# source .bashrc
source $HOME/.bashrc

# update conda (just because)
conda update -n base conda
```

### 4 clone this repo
```sh
git clone https://github.com/WatsonLab/MAGpy.git
```

### 5 create the main MAGpy environment
```sh
conda env create -f MAGpy/envs/install.yaml

# activate it
conda activate magpy_install
```

### 6 download data and build indices
```sh
# Uniprot - TREMBL
# NOTE - may require a large amount of RAM
wget -q ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz 
diamond makedb --in uniprot_trembl.fasta.gz -d uniprot_trembl
rm uniprot_trembl.fasta.gz

# Sourmash
wget -q https://s3-us-west-2.amazonaws.com/sourmash-databases/2018-03-29/genbank-d2-k31.tar.gz
gunzip < genbank-d2-k31.tar.gz | tar xvf -


# Pfam
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.dat.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/active_site.dat.gz
gunzip Pfam-A.hmm.gz Pfam-A.hmm.dat.gz active_site.dat.gz
hmmpress Pfam-A.hmm

# get checkM data
mkdir checkm_data
cd checkm_data
wget https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz
gunzip < checkm_data_2015_01_16.tar.gz | tar xvf -
cd ..
```

### 7 update ete3 database
```
python MAGpy/scripts/update_ete3.py
```
NB there is currently an issue with ete3, see https://github.com/etetoolkit/ete/issues/469

### 8 install phylophlan
```
hg clone https://bitbucket.org/nsegata/phylophlan
```

### 9 edit config.json

The file config.json tells MAGpy where everything is.  On this installation on Ubuntu, it should (and does) look like this:

```sh
{
    "phylophlan_dir": "./phylophlan",
    "uniprot_sprot": "/home/ubuntu/uniprot_trembl",
    "sourmash_gbk": "/home/ubuntu/genbank-k31.sbt.json",
    "pfam_dir": "/home/ubuntu/",
    "checkm_dataroot": "./checkm_data"
}
```

### 10 make scripts executeable

```sh
chmod 755 MAGpy/scripts/*
chmod 755 MAGpy/test/scripts/*
```

### 11 Install Color::Mix

If you want to draw a tree of MAGs using GraPhlAn and our script "produce_tree.pl" then you will need to install Perl module "Color::Mix"

```
conda env create -f MAGpy/envs/basic2.yaml
source activate basic2

/usr/bin/env perl -MCPAN -e 'install Color::Mix'
# answer yes to automatic config
```





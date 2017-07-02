#!/bin/bash

# run from git root directory. Command: ./devenv/setup-devenv.sh

wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh -b -p miniconda2
source miniconda2/bin/activate
echo "source `readlink -e miniconda2/bin/activate`" > adv_celppade_env.sh

# Install latest RDKit.
# RDKit versions before 2016.03.01 can make rare ligand prep mistakes.
conda install -y -c rdkit rdkit-postgresql

# Install core D3R utilities for challengedata handling
pip install d3r

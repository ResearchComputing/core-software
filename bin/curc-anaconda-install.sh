#!/bin/bash

bash /curc/sw/anaconda2/Anaconda2-2019.03-Linux-x86_64.sh -b -p /curc/sw/anaconda2/2019.03
(
    eval "$(/curc/sw/anaconda2/2019.03/bin/conda shell.bash hook)"
    conda config --add channels intel
    conda create -n idp intelpython2_full python=2

    conda install r rstudio
)

bash /curc/sw/anaconda3/Anaconda3-2019.03-Linux-x86_64.sh -b -p /curc/sw/anaconda3/2019.03
(
    eval "$(/curc/sw/anaconda3/2019.03/bin/conda shell.bash hook)"
    conda config --add channels intel
    conda create -n idp intelpython3_full python=3

    conda install r rstudio
)

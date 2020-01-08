Bootstrap: docker
From: python:3.7

%help
    EEGprep preprocessing container

%setup
    python setup.py sdist

%files
    dist/eegprep-0.1.tar.gz .

%post
    pip install eegprep-0.1.tar.gz

%runscript
    exec eegprep

%labels
    Version 0.1

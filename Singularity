Bootstrap: docker
From: python:3

%help
    EEGprep preprocessing container

%files
    requirements.txt
    eegprep/preproc.py .

%post
    pip install --no-cache-dir -r requirements.txt

%runscript
    exec python preproc.py

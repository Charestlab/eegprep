Bootstrap: docker
From: python:3

%help
    EEGprep preprocessing container

%files
    requirements.txt
    eegprep/preproc.py .

%post
    pip install --no-cache-dir -U https://api.github.com/repos/mne-tools/mne-python/zipball/master#egg=mne
    pip install --no-cache-dir -r requirements.txt
    python setup.py develop

%runscript
    exec python preproc.py

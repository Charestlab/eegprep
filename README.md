# EEGprep
Standardized EEG preprocessing in a virtual machine image


## Singularity

Build the EEGprep singularity image:
```
sudo singularity build illmotion.simg Singularity
```

Run EEGprep on your data:
```
singularity run -c -e --bind /your/data/dir/:/data illmotion.simg
```
where /your/data/dir/ contains a *BIDS* folder.


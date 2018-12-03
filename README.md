# EEGprep
Standardized EEG preprocessing


## Singularity

Build the EEGprep singularity image:
```
sudo singularity build eegprep.simg Singularity
```

Run EEGprep on your data:
```
singularity run -c -e --bind /your/data/dir/:/data eegprep.simg
```
where /your/data/dir/ contains a *BIDS* folder.

## Configuration

You can give EEGprep some direction by putting a configuration file
in your data direction called `eegprep.conf`. See also `example.eegprep.conf` 
in this repository.

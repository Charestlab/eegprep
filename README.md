# EEGprep
Standardized EEG preprocessing

[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3833)


## Singularity

Download the EEGprep singularity image:
```
singularity pull --name eegprep.simg shub://Charestlab/eegprep
```

Run EEGprep on your data:
```
singularity run -c -e --bind /your/data/dir/:/data eegprep.simg
```

## Commandline

You can run eegprep on the commandline. Start by running `eegprep -h` and you'll see:
```
usage: eegprep [-h] [-s SUBJECT_INDEX] [-l SUBJECT_LABEL] [data_directory]

positional arguments:
  data_directory        root data directory

optional arguments:
  -h, --help            show this help message and exit
  -s SUBJECT_INDEX, --subject-index SUBJECT_INDEX
                        index of subject to work on when sorted alphabetically
  -l SUBJECT_LABEL, --subject-label SUBJECT_LABEL
                        label of subject to work on

```

## Configuration

You can give EEGprep some direction by putting a configuration file
in your data direction called `eegprep.conf`. See also `example.eegprep.conf` 
in this repository.

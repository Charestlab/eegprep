from os.path import join, basename
import os, glob
import numpy
import mne
import pandas
from eegprep.bids.naming import filename2tuple
from eegprep.guess import guess_montage
from eegprep.configuration import Configuration
from eegprep.defaults import defaults


datadir = '/data'

conf_file_path = join(datadir, 'eegprep.conf')
config = Configuration()
config.setDefaults(defaults)
if os.path.isfile(conf_file_path):
    with open(conf_file_path) as fh:
        conf_string = fh.read()
    config.updateFromString(conf_string)
print(config)

bidsdir = join(datadir, 'BIDS')


subjectdirs = glob.glob(join(bidsdir, 'sub-*'))
for subjectdir in subjectdirs:
    assert os.path.isdir(subjectdir)
    sub = basename(subjectdir)[4:]

    # prepare derivatives directory
    derivdir = join(bidsdir, 'derivatives', 'sub-' + sub)
    os.makedirs(derivdir, exist_ok=True)

    subject_epochs = {}
    for fname in glob.glob(join(subjectdir, 'eeg', '*.set')):
        sub, ses, task, run = filename2tuple(basename(fname))

        # read data
        raw = mne.io.read_raw_eeglab(fname, preload=True, verbose=False)
        events = mne.find_events(raw)  #raw, consecutive=False, min_duration=0.005)

        # Set channel types and select reference channels
        channelFile = fname.replace('eeg.set', 'channels.tsv')
        channels = pandas.read_csv(channelFile, index_col='name', sep='\t')
        bids2mne = {
            'MISC': 'misc',
            'EEG': 'eeg',
            'VEOG': 'eog',
            'TRIG': 'stim',
            'REF': 'eeg',
        }
        channels['mne'] = channels.type.replace(bids2mne)
        raw.set_channel_types(channels.mne.to_dict())
        refChannels = channels[channels.type=='REF'].index.tolist()

        # Filtering
        raw.filter(l_freq=0.1, h_freq=40, fir_design='firwin')
        raw.pick_types(eeg=True, eog=True)
        montage = mne.channels.read_montage(guess_montage(raw.ch_names))
        raw.set_montage(montage)

        # Set reference
        raw.set_eeg_reference(ref_channels=refChannels)

        ##  epoching
        reject = dict(eeg=180e-6, eog=100e-6) # 1e-5
        epochs_params = dict(events=events, tmin=-0.1, tmax=0.5, reject=reject)
        file_epochs = mne.Epochs(raw, **epochs_params)

        subject_epochs[(ses, task, run)] = file_epochs

    taskSeg = 1
    tasks = set([k[taskSeg] for k in subject_epochs.keys()])
    for task in tasks:
        task_epochs_list = [v for (k, v) in subject_epochs.items() if k[taskSeg]==task]
        task_epochs = mne.epochs.concatenate_epochs(task_epochs_list)
        task_epochs = task_epochs.pick_types(eeg=True, exclude=refChannels)
        task_epochs.save(join(derivdir, 'sub-{}_task-{}_epo.fif'.format(sub, task)))

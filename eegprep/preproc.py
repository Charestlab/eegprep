from os.path import join, basename
import os, glob
import numpy
import mne
import pandas
from eegprep.bids.naming import filename2tuple
from eegprep.guess import guess_montage

datadir = '/media/charesti-start/data/irsa-eeg/'
bidsdir = join(datadir, 'BIDS')

channels = pandas.read_csv('_channels.tsv', sep='\t')

subjectdirs = glob.glob(join(bidsdir, 'sub-*'))
for subjectdir in subjectdirs:
    assert os.path.isdir(subjectdir)
    sub = basename(subjectdir)[4:]

    # prepare derivatives directory
    derivdir = join(bidsdir, 'derivatives', sub)
    os.makedirs(derivdir, exist_ok=True)

    subject_epochs = {}
    for fname in glob.glob(join(subjectdir, 'eeg', '*.set')):
        sub, ses, task, run = filename2tuple(basename(fname))

        # read data
        raw = mne.io.read_raw_eeglab(fname, preload=True, verbose=False)
        events = mne.find_events(raw)  #raw, consecutive=False, min_duration=0.005)

        # Set channel types and select reference channels
        channelFile = fname.replace('eeg.set', 'channels.tsv')
        channels = pandas.read_csv(channelFile, sep='\t')
        bids2mne = {
            'MISC': 'misc',
            'EEG': 'eeg',
            'VEOG': 'eog',
            'TRIG': 'stim',
            'REF': 'eeg',
        }
        channels['mne'] = channels.type.replace(bids2mne)
        mneMapping = pandas.Series(channels,mne, index=channels.name).to_dict()
        raw.set_channel_types(mneMapping)
        refChannels = channels[channels.type=='REF'].name

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
        break
    break

    taskSeg = 1
    tasks = set([k[taskSeg] for k in subject_epochs.keys()])
    for task in tasks:
        task_epochs_list = [v for (k, v) in subject_epochs.items() if k[taskSeg]==task]
        task_epochs = mne.epochs.concatenate_epochs(task_epochs_list)
        task_epochs = task_epochs.pick_types(eeg=True, exclude=refChannels)
        task_epochs.save(join(derivdir, 'sub-{}_task-{}_epo.fif'.format(sub, task)))

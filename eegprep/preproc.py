from os.path import join, basename
import os, glob
import numpy
import mne
from eegprep.bids.naming import filename2tuple

datadir = '/data/'
bidsdir = join(datadir, 'BIDS')

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

        # Create EOG channel from EXG3
        raw.set_channel_types(mapping={'EXG3': 'eog'})
        raw.filter(l_freq=0.1, h_freq=40, fir_design='firwin')
        raw.pick_types(eeg=True, eog=True)
        biosemi64 = mne.channels.read_montage('biosemi64')
        raw.set_montage(biosemi64)
        raw.set_eeg_reference(ref_channels=['EXG1', 'EXG2'])

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
        task_epochs = task_epochs.pick_types(eeg=True, exclude=['EXG1', 'EXG2', 'EXG3'])
        task_epochs.save(join(derivdir, 'sub-{}_task-{}_epo.fif'.format(sub, task)))

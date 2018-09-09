from os.path import join, basename
import os, glob
import numpy
import scipy.io
import mne
import pandas
from eegprep.bids.naming import filename2tuple
from eegprep.guess import guess_montage
from eegprep.configuration import Configuration
from eegprep.defaults import defaults


# datadir = '/data'
datadir = '/media/charesti-start/data/irsa-eeg/'

conf_file_path = join(datadir, 'eegprep.conf')
config = Configuration()
config.setDefaults(defaults)
if os.path.isfile(conf_file_path):
    with open(conf_file_path) as fh:
        conf_string = fh.read()
    config.updateFromString(conf_string)
print(config)

bidsdir = join(datadir, 'BIDS')


subjectdirs = sorted(glob.glob(join(bidsdir, 'sub-*')))
for subjectdir in subjectdirs:
    assert os.path.isdir(subjectdir)
    sub = basename(subjectdir)[4:]

    # prepare derivatives directory
    derivdir = join(bidsdir, 'derivatives', 'eegprep', 'sub-' + sub)
    os.makedirs(derivdir, exist_ok=True)

    subject_epochs = {}
    for fname in sorted(glob.glob(join(subjectdir, 'eeg', '*.set'))):
        sub, ses, task, run = filename2tuple(basename(fname))

        print('\nProcessing raw file: ' + basename(fname))

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
        epochs_params = dict(
            events=events,
            tmin=-0.1,
            tmax=0.5,
            reject=dict(eeg=250e-6, eog=150e-6)
        )
        file_epochs = mne.Epochs(raw, preload=True, **epochs_params)
        file_epochs.pick_types(eeg=True, exclude=refChannels)

        # downsample if configured to do so
        if config['downsample'] < raw.info['sfreq']:
            file_epochs = file_epochs.copy().resample(config['downsample'], npad='auto')

        if len(file_epochs):
            subject_epochs[(ses, task, run)] = file_epochs

    taskSeg = 1
    tasks = list(set([k[taskSeg] for k in subject_epochs.keys()]))
    for task in tasks:
        print('\nGathering epochs for task: ' + task)
        task_epochs_list = [v for (k, v) in subject_epochs.items() if k[taskSeg]==task]
        nsamples = len(task_epochs_list[0].times)  
        nchannels = len(task_epochs_list[0].ch_names)
        nepochs = numpy.array([len(e) for e in task_epochs_list])
        task_data = numpy.full([nepochs.sum(), nchannels, nsamples], numpy.nan)
        task_events = numpy.full([nepochs.sum()], numpy.nan)
        offset = 0
        for r, epochs in enumerate(task_epochs_list):
            epoch_idx = numpy.arange(nepochs.sum())[offset:offset+nepochs[r]]
            task_data[epoch_idx, :, :] = epochs.get_data()
            task_events[epoch_idx] = epochs.events[:, 2]
            fname = join(derivdir, 'sub-{}_task-{}_epo.mat'.format(sub, task))
            offset += nepochs[r]
        scipy.io.savemat(fname, mdict={'epochs': task_data, 'events': task_events})

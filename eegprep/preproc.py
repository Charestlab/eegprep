from os.path import join, basename
import os, glob
import numpy
import scipy.io
import mne
import pandas
from eegprep.bids.naming import filename2tuple
from eegprep.guess import guess_montage
from eegprep.util import resample_events_on_resampled_epochs
from eegprep.configuration import Configuration
from eegprep.defaults import defaults


#datadir = '/data'
#datadir = '/media/charesti-start/data/irsa-eeg/'
datadir = '/home/adf/vandejjf/Data/irsa-eeg/'

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
        
        try:
            # the below fails if the specified channels are not in the data
            raw.set_channel_types(channels.mne.to_dict())
        except ValueError as exception:
            print(exception)
            continue
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
            tmax=0.8,
            reject=None  # dict(eeg=250e-6, eog=150e-6)
        )
        file_epochs = mne.Epochs(raw, preload=True, **epochs_params)
        file_epochs.pick_types(eeg=True, exclude=refChannels)

        if len(file_epochs):
            subject_epochs[(ses, task, run)] = file_epochs


    sessSeg = 0
    sessions = sorted(list(set([k[sessSeg] for k in subject_epochs.keys()])))
    for session in sessions:
        taskSeg = 1
        tasks = list(set([k[taskSeg] for k in subject_epochs.keys() if k[sessSeg]==session]))
        for task in tasks:
            print('\nGathering epochs for session {} task {}'.format(session, task))
            epochs_selection = [v for (k, v) in subject_epochs.items() if k[:2]==(session, task)]

            task_epochs = mne.epochs.concatenate_epochs(epochs_selection)
            
            # downsample if configured to do so
            # important to do this after concatenation because 
            # downsampling may cause rejection for 'TOOSHORT'
            if config['downsample'] < task_epochs.info['sfreq']:
                task_epochs = task_epochs.copy().resample(config['downsample'], npad='auto')

            ext = config['out_file_format']
            fname = join(derivdir, 'sub-{}_ses-{}_task-{}_epo.{}'.format(sub, session, task, ext))
            variables = {
                'epochs': task_epochs.get_data(),
                'events': task_epochs.events,
                'timepoints': task_epochs.times
            }
            if ext == 'fif':
                task_epochs.save(fname)
            elif ext == 'mat':
                scipy.io.savemat(fname, mdict=variables)
            elif ext == 'npy':
                numpy.savez(fname, **variables)


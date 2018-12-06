from os.path import join, basename, splitext
import os, glob, random
import numpy
import scipy.io
import mne
import pandas
from autoreject import AutoReject
from eegprep.bids.naming import filename2tuple
from eegprep.guess import guess_montage
from eegprep.util import (
    resample_events_on_resampled_epochs,
    plot_rejectlog,
    save_rejectlog
)
from eegprep.configuration import Configuration
from eegprep.defaults import defaults


def run_preproc(datadir='/data'):

    print('data directory: {}'.format(datadir))
    conf_file_path = join(datadir, 'eegprep.conf')
    config = Configuration()
    config.setDefaults(defaults)
    if os.path.isfile(conf_file_path):
        with open(conf_file_path) as fh:
            conf_string = fh.read()
        config.updateFromString(conf_string)
    print('configuration:')
    print(config)

    bidsdir = join(datadir, 'BIDS')
    eegprepdir = join(bidsdir, 'derivatives', 'eegprep')

    
    subjectdirs = sorted(glob.glob(join(bidsdir, 'sub-*')))
    for subjectdir in subjectdirs:
        assert os.path.isdir(subjectdir)
        
        sub = basename(subjectdir)[4:]

        # prepare derivatives directory
        derivdir = join(eegprepdir, 'sub-' + sub)
        os.makedirs(derivdir, exist_ok=True)
        reportsdir = join(eegprepdir, 'reports', 'sub-' + sub)
        os.makedirs(reportsdir, exist_ok=True)


        subject_epochs = {}
        rawtypes = {'.set': mne.io.read_raw_eeglab, '.bdf': mne.io.read_raw_edf}
        for fname in sorted(glob.glob(join(subjectdir, 'eeg', '*'))):
            _, ext = splitext(fname)
            if ext not in rawtypes.keys():
                continue
            sub, ses, task, run = filename2tuple(basename(fname))

            print('\nProcessing raw file: ' + basename(fname))

            # read data
            raw = rawtypes[ext](fname, preload=True, verbose=False)
            events = mne.find_events(raw)  #raw, consecutive=False, min_duration=0.005)

            # Set channel types and select reference channels
            channelFile = fname.replace('eeg' + ext, 'channels.tsv')
            channels = pandas.read_csv(channelFile, index_col='name', sep='\t')
            bids2mne = {
                'MISC': 'misc',
                'EEG': 'eeg',
                'VEOG': 'eog',
                'TRIG': 'stim',
                'REF': 'eeg',
            }
            channels['mne'] = channels.type.replace(bids2mne)
            
            # the below fails if the specified channels are not in the data
            raw.set_channel_types(channels.mne.to_dict())

            # set bad channels
            raw.info['bads'] = channels[channels.status=='bad'].index.tolist()

            # pick channels to use for epoching
            epoching_picks = mne.pick_types(raw.info, eeg=True, eog=True, stim=False, exclude='bads')


            # Filtering
            raw.filter(l_freq=0.05, h_freq=40, fir_design='firwin')

            montage = mne.channels.read_montage(guess_montage(raw.ch_names))
            print(montage)
            raw.set_montage(montage)

            # plot raw data
            nchans = len(raw.ch_names)
            pick_channels = numpy.arange(0, nchans, numpy.floor(nchans/20)).astype(int)
            start = numpy.round(raw.times.max()/2)
            fig = raw.plot(start=start, order=pick_channels)
            fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_raw.png'.format(sub, ses, task, run)
            fig.savefig(join(reportsdir, fname_plot))

            # Set reference
            refChannels = channels[channels.type=='REF'].index.tolist()
            raw.set_eeg_reference(ref_channels=refChannels)

            ##  epoching
            epochs_params = dict(
                events=events,
                tmin=-0.2,
                tmax=1,
                reject=None  # dict(eeg=250e-6, eog=150e-6)
                picks=epoching_picks,
            )
            file_epochs = mne.Epochs(raw, **epochs_params)


            if not len(file_epochs):
                continue

            # autoreject (under development)
            ar = AutoReject()
            clean_epochs = ar.fit_transform(file_epochs)
            try:
                rejectlog = ar.get_reject_log(clean_epochs)
                fname_log = 'sub-{}_ses-{}_task-{}_run-{}_reject-log.npz'.format(sub, ses, task, run)
                save_rejectlog(join(reportsdir, fname_log), rejectlog)
                fig = plot_rejectlog(rejectlog)
                fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_bad-epochs.png'.format(sub, ses, task, run)
                fig.savefig(join(reportsdir, fname_plot))
            except Exception as exception:
                print(exception)

            # store for now
            clean_epochs.drop_channels(refChannels)
            subject_epochs[(ses, task, run)] = clean_epochs

            # create evoked plots
            conds = clean_epochs.event_id.keys()
            selected_conds = random.sample(conds, min(len(conds), 3))
            picks = mne.pick_types(clean_epochs.info, eeg=True)
            for cond in selected_conds:
                evoked = clean_epochs[cond].average()
                fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_evoked-{}.png'.format(sub, ses, task, run, cond)
                fig = evoked.plot_joint(picks=picks)
                fig.savefig(join(reportsdir, fname_plot))



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


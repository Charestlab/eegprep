from os.path import join, basename, splitext
import os, glob, random, numpy, mne, pandas
from eegprep.bids.naming import filename2tuple
from eegprep.guess import guess_montage
from eegprep.util import (
    resample_events_on_resampled_epochs,
    plot_rejectlog,
    save_rejectlog
)


def preproc_run(fpath, config):

    #sub, ses, task, run = filename2tuple(basename(fname))

    # read data
    raw = mne.io.read_raw_bdf(fpath, preload=True, verbose=False)

    # Set channel types and select reference channels
    channelFile = fpath.replace('eeg.bdf', 'channels.tsv') # maybe should be a string arg
    channels = pandas.read_csv(channelFile, index_col='name', sep='\t')
    bids2mne = {
        'MISC': 'misc',
        'EEG': 'eeg',
        'EOG': 'eog',
        'VEOG': 'eog',
        'TRIG': 'stim',
        'REF': 'eeg',
    }
    channels['mne'] = channels.type.replace(bids2mne)
    raw.set_channel_types(channels.mne.to_dict())


    # Set reference
    refChannels = channels[channels.type=='REF'].index.tolist()
    raw = raw.set_eeg_reference(ref_channels=refChannels)


    # set bad channels
    # raw.info['bads'] = channels[channels.status=='bad'].index.tolist()

    # pick channels to use for epoching
    #epoching_picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, exclude='bads')


    # Filtering
    raw = raw.filter(l_freq=0.05, h_freq=45, fir_design='firwin')

    montage = mne.channels.read_montage(guess_montage(raw.ch_names))
    print(montage)
    raw.set_montage(montage)

    # plot raw data
    # nchans = len(raw.ch_names)
    # pick_channels = numpy.arange(0, nchans, numpy.floor(nchans/20)).astype(int)
    # start = numpy.round(raw.times.max()/2)
    # fig = raw.plot(start=start, order=pick_channels)
    # fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_raw.png'.format(sub, ses, task, run)
    # fig.savefig(join(reportsdir, fname_plot))


    events = mne.find_events(raw)  #raw, consecutive=False, min_duration=0.005)
    ##  epoching
    # epochs_params = dict(
    #     events=events,
    #     tmin=-0.1,
    #     tmax=0.8,
    #     reject=None,  # dict(eeg=250e-6, eog=150e-6)
    #     picks=epoching_picks,
    #     detrend=0,
    # )
    # file_epochs = mne.Epochs(raw, preload=True, **epochs_params)
    # file_epochs.drop_channels(refChannels)

    # # autoreject (under development)
    # ar = AutoReject(n_jobs=4)
    # clean_epochs = ar.fit_transform(file_epochs)

    # rejectlog = ar.get_reject_log(clean_epochs)
    # fname_log = 'sub-{}_ses-{}_task-{}_run-{}_reject-log.npz'.format(sub, ses, task, run)
    # save_rejectlog(join(reportsdir, fname_log), rejectlog)
    # fig = plot_rejectlog(rejectlog)
    # fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_bad-epochs.png'.format(sub, ses, task, run)
    # fig.savefig(join(reportsdir, fname_plot))


    # # store for now
    # # subject_epochs[(ses, task, run)] = clean_epochs

    # # create evoked plots
    # conds = clean_epochs.event_id.keys()
    # selected_conds = random.sample(conds, min(len(conds), 6))
    # picks = mne.pick_types(clean_epochs.info, eeg=True)
    # for cond in selected_conds:
    #     evoked = clean_epochs[cond].average()
    #     fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_evoked-{}.png'.format(sub, ses, task, run, cond)
    #     fig = evoked.plot_joint(picks=picks)
    #     fig.savefig(join(reportsdir, fname_plot))


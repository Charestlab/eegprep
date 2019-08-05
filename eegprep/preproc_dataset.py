from os.path import join, basename, splitext
import os, glob, random
from eegprep.configuration import Configuration
from eegprep.defaults import defaults
from eegprep.preproc_run import preproc_run


def preproc_dataset(datadir='/data'):

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
        rawtypes = {'.set': mne.io.read_raw_eeglab, '.bdf': mne.io.read_raw_bdf}
        for fname in sorted(glob.glob(join(subjectdir, 'eeg', '*'))):


            preproc_run(fname, config)

            _, ext = splitext(fname)
            if ext not in rawtypes.keys():
                continue
            sub, ses, task, run = filename2tuple(basename(fname))

            # store for now
            subject_epochs[(ses, task, run)] = clean_epochs

            # # create evoked plots
            # conds = clean_epochs.event_id.keys()
            # selected_conds = random.sample(conds, min(len(conds), 6))
            # picks = mne.pick_types(clean_epochs.info, eeg=True)
            # for cond in selected_conds:
            #     evoked = clean_epochs[cond].average()
            #     fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_evoked-{}.png'.format(sub, ses, task, run, cond)
            #     fig = evoked.plot_joint(picks=picks)
            #     fig.savefig(join(reportsdir, fname_plot))



        # sessSeg = 0
        # sessions = sorted(list(set([k[sessSeg] for k in subject_epochs.keys()])))
        # for session in sessions:
        #     taskSeg = 1
        #     tasks = list(set([k[taskSeg] for k in subject_epochs.keys() if k[sessSeg]==session]))
        #     for task in tasks:
        #         print('\nGathering epochs for session {} task {}'.format(session, task))
        #         epochs_selection = [v for (k, v) in subject_epochs.items() if k[:2]==(session, task)]

        #         task_epochs = mne.epochs.concatenate_epochs(epochs_selection)
                
        #         # downsample if configured to do so
        #         # important to do this after concatenation because 
        #         # downsampling may cause rejection for 'TOOSHORT'
        #         if config['downsample'] < task_epochs.info['sfreq']:
        #             task_epochs = task_epochs.copy().resample(config['downsample'], npad='auto')

        #         ext = config['out_file_format']
        #         fname = join(derivdir, 'sub-{}_ses-{}_task-{}_epo.{}'.format(sub, session, task, ext))
        #         variables = {
        #             'epochs': task_epochs.get_data(),
        #             'events': task_epochs.events,
        #             'timepoints': task_epochs.times
        #         }
        #         if ext == 'fif':
        #             task_epochs.save(fname)
        #         elif ext == 'mat':
        #             scipy.io.savemat(fname, mdict=variables)
        #         elif ext == 'npy':
        #             numpy.savez(fname, **variables)


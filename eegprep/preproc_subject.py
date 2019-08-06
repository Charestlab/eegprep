from eegprep.preproc_run import preproc_run
import numpy


def preproc_subject(layout, subject, out_fpath):

    print('preprocessing subject {}'.format(subject))

    eeg_runs = layout.get(subject=subject, suffix='eeg', extension='bdf')
    epochs_all = []
    events_all = []
    for eeg_run in eeg_runs:
        epochs_run = preproc_run(eeg_run.path)
        epochs_all.append(epochs_run.get_data())
        events_all.append(epochs_run.events[:, 2])
    # else:
    #     return

    variables = {
        'epochs': numpy.concatenate(epochs_all, axis=0),
        'events': numpy.concatenate(events_all, axis=0),
    }
    # not using fif because of eegprep#10
    numpy.savez(out_fpath, **variables)

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



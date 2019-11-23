from eegprep.jobs.base import BaseJob


class EpochJob(BaseJob):

    def run(self):
        events = mne.find_events(raw, verbose=False)  #raw, consecutive=False, min_duration=0.005)
        ##  epoching
        picks = mne.pick_types(raw.info, eeg=True)
        epochs_params = dict(
            events=events,
            tmin=-0.2,
            tmax=0.8,
            picks=picks,
            verbose=False
        )
        epochs = mne.Epochs(raw, preload=True, **epochs_params)
        #epochs = epochs.resample(256., npad='auto') # downsample
        # file_epochs.drop_channels(refChannels)

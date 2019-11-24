from eegprep.jobs.base import BaseJob
import mne


class EpochJob(BaseJob):

    def run(self):
        raw = self.io.retrieve_object('raw')
        # additional options: consecutive=False, min_duration=0.005)
        events = mne.find_events(raw, verbose=False)
        picks = mne.pick_types(raw.info, eeg=True)
        epochs_params = dict(
            events=events,
            tmin=-0.2,
            tmax=3.1,
            picks=picks,
            verbose=False
        )
        epochs = mne.Epochs(raw, preload=True, **epochs_params)
        self.io.store_object(epochs, name='epo', job=self)

from eegprep.jobs.base import BaseJob
import mne


class ConcatEpochsJob(BaseJob):
    
    def run(self):
        epochs_per_run = self.io.retrieve_objects('epochs')
        epochs = mne.epochs.concatenate_epochs(epochs_per_run)
        self.io.store_object(epochs, name='epochs', job=self)

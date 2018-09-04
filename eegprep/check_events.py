import scipy
from mne.io.eeglab.eeglab import _read_annotations_eeglab
fpath = '/media/charesti-start/data/irsa-eeg/BIDS/sub-01/eeg/sub-01_ses-01_task-irsa_run-01_eeg.set'
eeg = scipy.io.loadmat(fpath, struct_as_record=False, squeeze_me=True)['EEG']

annotations = _read_annotations_eeglab(eeg)
types = annotations.description
latencies = annotations.onset
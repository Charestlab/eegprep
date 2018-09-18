import numpy


def resample_events_on_resampled_epochs(epochs, orig_sfreq):
    """
    Based on mne.BaseRaw.resample fragment
    """
    ratio = float(epochs.info['sfreq']) / orig_sfreq
    events = epochs.events.copy()
    events[:, 0] = numpy.round(events[:, 0] * ratio).astype(int)
    epochs.events = events

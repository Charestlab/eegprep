import numpy
import matplotlib.pyplot as plt


def resample_events_on_resampled_epochs(epochs, orig_sfreq):
    """
    Based on mne.BaseRaw.resample fragment
    """
    ratio = float(epochs.info['sfreq']) / orig_sfreq
    events = epochs.events.copy()
    events[:, 0] = numpy.round(events[:, 0] * ratio).astype(int)
    epochs.events = events

def plot_rejectlog(rejectlog):
    """Plot.
    based on https://github.com/autoreject/autoreject/blob/master/autoreject/autoreject.py#L1160

    original uses plt.show() instead of returning fig
    """

    fig = plt.figure(figsize=(12, 6))
    ax = fig.gca()
    ax.imshow(
        rejectlog.labels,
        cmap='Reds',
        interpolation='nearest'
    )
    # XXX to be fixed
    ch_names_ = rejectlog.ch_names[7::10]
    
    ax.grid(False)
    ax.set_xlabel('Channels')
    ax.set_ylabel('Epochs')
    ax.set(
        xticks=range(7, rejectlog.labels.shape[1], 10),
        xticklabels=ch_names_
    )
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.tick_params(axis=u'both', which=u'both', length=0)
    fig.tight_layout(rect=[None, None, None, 1.1])
    return fig

def save_rejectlog(rejectlog, filepath):
    numpy.savez(
        filepath,
        bad_epochs=rejectlog.bad_epochs,
        labels=rejectlog.labels,
        ch_names=rejectlog.ch_names
    )


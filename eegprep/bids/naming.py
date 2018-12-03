BIDS_SEGMENTS = ['sub', 'ses', 'task', 'run']


def filename2tuple(fname):
    segments = fname.split('_')
    vals = [None] * len(BIDS_SEGMENTS)
    for seg in segments:
        for l in [3, 4]:
            if seg[:l] in BIDS_SEGMENTS:
                vals[BIDS_SEGMENTS.index(seg[:l])] = seg[l+1:]
    return tuple(vals)


def args2filename(**kwargs):
    fname = ''
    for seg in BIDS_SEGMENTS:
        if seg in kwargs:
            fname += seg + '-' + kwargs[seg]
    return fname
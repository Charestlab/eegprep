

def guess_montage(ch_names):
    return 'biosemi64' if  len(ch_names) < 100 else 'biosemi128'
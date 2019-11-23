#from bids import BIDSLayout

# TODO:     # contains input, output, mem_storage, report

#   io.store(for_run=run, epochs) # io decides whether to keep in memory (with mem limit arg) or to store temp or store long term

class InputOutput(object):

    def __init__(self, root_dir):
        pass
    
    def get_subject_labels(self):
        # TODO: must be sorted
        return ''

    def for_(self, subject=None):
        pass

#    subjects = layout.get(return_type='id', target='subject')

# -    # output
# -    eegprepdir = join(args.data_directory, 'derivatives', 'eegprep')
# -    subjectdir = join(eegprepdir, 'sub-' + subject)
# -    os.makedirs(subjectdir, exist_ok=True)
# -    out_fpath = join(subjectdir, 'sub-{}_epo.npz'.format(subject))
    # eegprepdir = join(datadir, 'derivatives', 'eegprep')
    # layout = BIDSLayout(datadir)
    # subjects = layout.get(return_type='id', target='subject')
    # for subject in subjects:

    #     subjectdir = join(eegprepdir, 'sub-' + subject)
    #     os.makedirs(subjectdir, exist_ok=True)
    #     out_fpath = join(subjectdir, 'sub-{}_epo.npz'.format(subject))
    #     preproc_subject(layout, subject, out_fpath)

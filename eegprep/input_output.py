from bids import BIDSLayout

# TODO:     # contains input, output, mem_storage, report

#   io.store(for_run=run, epochs) # io decides whether to keep in memory (with mem limit arg) or to store temp or store long term

class InputOutput(object):

    def __init__(self, log, root_dir):
        self.log = log
        self.root_dir = root_dir
        self._layout = None

    @property
    def layout(self):
        if self._layout is None:
            self.log.discovering_data()
            self._layout = BIDSLayout(self.root_dir)
        return self._layout
    
    def get_subject_labels(self):
        subjects = self.layout.get(return_type='id', target='subject')
        self.log.found_subjects(subjects)
        return subjects

    def get_run_labels(self):
        return self.layout.get(return_type='id', target='run')

    def for_(self, subject=None, run=None):
        return self

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

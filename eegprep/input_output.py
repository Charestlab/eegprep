from bids import BIDSLayout
import copy

# TODO:     # contains input, output, mem_storage, report

#   io.store(for_run=run, epochs) # io decides whether to keep in memory (with mem limit arg) or to store temp or store long term

class InputOutput(object):

    def __init__(self, log, root_dir, scope=None, layout=None):
        self.log = log
        self.root_dir = root_dir
        self._layout = layout or None
        self.scope = scope or dict()

    @property
    def layout(self):
        if self._layout is None:
            self.log.discovering_data()
            self._layout = BIDSLayout(self.root_dir)
        return self._layout

    def describe_scope(self):
        return ' '.join([f'{k[:3]}={v}' for k, v in self.scope.items()])
    
    def get_subject_labels(self):
        subjects = self.layout.get(return_type='id', target='subject')
        self.log.found_subjects(subjects)
        return subjects

    def get_run_labels(self):
        return self.layout.get(return_type='id', target='run')

    def for_(self, subject=None, run=None):
        new_scope = copy.copy(self.scope)
        for spec, val in dict(subject=subject, run=run).items():
            if val is not None:
                new_scope[spec] = val
        return InputOutput(self.log, self.root_dir, new_scope, self.layout)

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

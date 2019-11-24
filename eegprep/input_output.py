from bids import BIDSLayout
import copy


class InputOutput(object):

    def __init__(self, log, memory, root_dir, scope=None, layout=None):
        self.log = log
        self.memory = memory
        self.root_dir = root_dir
        self._layout = layout or None
        self.scope = scope or dict()

    @property
    def layout(self):
        """pyBIDS layout object, lazily loaded.

        If the layout has not been created yet, it will
        be done here, which takes time (<1min) for larger datasets.
        
        Returns:
            bids.BIDSLayout: The BIDS layout object
        """
        if self._layout is None:
            self.log.discovering_data()
            self._layout = BIDSLayout(self.root_dir)
        return self._layout

    def describe_scope(self):
        return ' '.join([f'{k[:3]}={v}' for k, v in self.scope.items()])
    
    def for_(self, subject=None, run=None):
        new_scope = copy.copy(self.scope)
        for spec, val in dict(subject=subject, run=run).items():
            if val is not None:
                new_scope[spec] = val
        return InputOutput(
            self.log,
            self.memory,
            self.root_dir,
            new_scope,
            self.layout
        )

    def get_subject_labels(self):
        subjects = self.layout.get(return_type='id', target='subject')
        self.log.found_subjects(subjects)
        return subjects

    def get_run_labels(self):
        return self.layout.get(return_type='id', target='run', **self.scope)

    def get_filepath(self, suffix):
        fpaths = self.layout.get(
            return_type='filename',
            suffix=suffix,
            **self.scope
        )
        assert len(fpaths) == 1
        return fpaths[0]

    def store_object(self, obj, name, job):
        # TODO: identify job by string
        identifiers = dict(name=name, **self.scope)
        self.memory.store(obj, **identifiers)

    def retrieve_objects(self, name):
        identifiers = dict(name=name, **self.scope)
        return self.memory.retrieve(**identifiers)

    def retrieve_object(self, name):
        objects = self.retrieve_objects(name)
        assert len(objects) == 1
        return objects[0]

# TODO:     # contains input, output, mem_storage, report
# TODO: job can choose when to expire objects 
# 
# (parent job? interface?) self.add_child() + job.cleanup() + io.store('obj', for_=self) CleanupJob?
# self.cleanup_after(child_job)
# self.store_later(child_job)
# super().add_to() or pipeline.add(self)
# add_children_to(self, pipeline)
# TODO:  io.store(for_run=run, epochs) # io decides whether to keep in memory (with mem limit arg) or to store temp or store long term
# eeg_runs = layout.get(subject=subject, suffix='eeg', extension='bdf')
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

from bids import BIDSLayout
import copy
from os.path import join, dirname, isdir
from os import makedirs


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
    
    def for_(self, subject=None, session=None, run=None):
        new_scope = copy.copy(self.scope)
        filters = dict(subject=subject, session=session, run=run)
        for spec, val in filters.items():
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
        subjects = self.layout.get(
            return_type='id',
            target='subject',
            datatype='eeg'
        )
        self.log.found_subjects(subjects)
        return subjects

    def get_session_labels(self):
        return self.layout.get(
            return_type='id',
            target='session',
            datatype='eeg',
            **self.scope
        )

    def get_run_labels(self):
        return self.layout.get(
            return_type='id', 
            target='run',
            datatype='eeg',
            **self.scope
        )

    def get_filepath(self, suffix):
        fpaths = self.layout.get(
            return_type='filename',
            suffix=suffix,
            datatype='eeg',
            **self.scope
        )
        fpaths = [f for f in fpaths if '.json' not in f]
        assert len(fpaths) == 1
        return fpaths[0]

    def store_object(self, obj, name, job):
        # first delete existing copies (overwriting)
        self.memory.delete(name=name, **self.scope)
        identifiers = dict(name=name, job=job.get_id(), **self.scope)
        self.memory.store(obj, **identifiers)

    def retrieve_objects(self, name):
        filters = dict(name=name, **self.scope)
        return self.memory.retrieve(**filters)

    def retrieve_object(self, name):
        objects = self.retrieve_objects(name)
        assert len(objects) == 1
        return objects[0]

    def expire_output_of(self, job):
        self.memory.delete(job=job.get_id(), **self.scope)

    def write_output_of(self, job):
        keys = self.memory.find_matching_keys(job=job.get_id(), **self.scope)
        for key in keys:
            self.write_object(key, self.memory.get(key))

    def write_object(self, descriptors, obj):
        fpath = self.build_fpath(suffix=descriptors.name, ext='fif')
        self.ensure_dir(dirname(fpath))
        self.log.writing_object(obj, fpath)
        obj.save(fpath)

    def ensure_dir(self, dirpath):
        if not isdir(dirpath):
            makedirs(dirpath)

    def build_fpath(self, suffix, ext):
        outdir = join(self.root_dir, 'derivatives', 'eegprep')
        for entity in ('subject', 'session'):
            if entity in self.scope:
                label = self.scope[entity]
                outdir = join(outdir, f'{entity[:3]}-{label}')
        fname = ''
        for entity in ('subject', 'session'):
            if entity in self.scope:
                label = self.scope[entity]
                fname += f'{entity[:3]}-{label}_'
        fname += f'{suffix}.{ext}'
        return join(outdir, fname)

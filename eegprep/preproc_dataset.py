from os.path import join, basename, splitext
import os, glob, random
# from eegprep.configuration import Configuration
# from eegprep.defaults import defaults
from eegprep.preproc_subject import preproc_subject
from bids import BIDSLayout


def preproc_dataset(datadir):

    # print('data directory: {}'.format(datadir))
    # conf_file_path = join(datadir, 'eegprep.conf')
    # config = Configuration()
    # config.setDefaults(defaults)
    # if os.path.isfile(conf_file_path):
    #     with open(conf_file_path) as fh:
    #         conf_string = fh.read()
    #     config.updateFromString(conf_string)
    # print('configuration:')
    # print(config)

    eegprepdir = join(datadir, 'derivatives', 'eegprep')
    layout = BIDSLayout(datadir)
    subjects = layout.get(return_type='id', target='subject')
    for subject in subjects:

        subjectdir = join(eegprepdir, 'sub-' + subject)
        os.makedirs(subjectdir, exist_ok=True)
        out_fpath = join(subjectdir, 'sub-{}_epochs.npz'.format(subject))
        preproc_subject(layout, subject, out_fpath)
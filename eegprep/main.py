from eegprep.args import parse_arguments
from os.path import join, basename, splitext
import os, glob, random
from eegprep.preproc_subject import preproc_subject
from bids import BIDSLayout


def run():
    args = parse_arguments()


    
    layout = BIDSLayout(args.data_directory)
    subjects = layout.get(return_type='id', target='subject')


    # IO
    # contains input, output, mem_storage, report
    # job = subject(io.for(subject=sub))
    #   io.store(for_run=run, epochs) # io decides whether to keep in memory or to store temp or store long term
    # pipeline.add(job)
    # pipeline.run()



    preproc_subject(layout, subject)

    # output
    eegprepdir = join(args.data_directory, 'derivatives', 'eegprep')
    subjectdir = join(eegprepdir, 'sub-' + subject)
    os.makedirs(subjectdir, exist_ok=True)
    out_fpath = join(subjectdir, 'sub-{}_epo.npz'.format(subject))
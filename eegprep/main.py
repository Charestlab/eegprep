from eegprep.args import parse_arguments
from eegprep.pipeline import Pipeline
from eegprep.input_output import InputOutput
from eegprep.jobs.subject import SubjectJob


def run(args=None):
    """Parses commandline arguments and runs EEGprep for the specified scope
    
    Args:
        args (Namespace, optional): Object with eeg prep parameters 
            as attributes. Defaults to None.
    """
    args = args or parse_arguments()
    print(args)
    io = InputOutput(
        root_dir = args.data_directory
    )
    pipeline = Pipeline(
        dry = args.dry_run
    )

    subjects = io.get_subject_labels()
    if args.subject_index:
        subjects = [subjects[args.subject_index]]

    if args.subject_label:
        subjects = [args.subject_label]

    for subject_label in subjects:
        job = SubjectJob(io.for_(subject=subject_label))
        job.add_to(pipeline)
    pipeline.run()

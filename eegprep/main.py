from eegprep.args import parse_arguments
from eegprep.pipeline import Pipeline
from eegprep.log import Log
from eegprep.input_output import InputOutput
from eegprep.jobs.subject import SubjectJob


def run(args=None):
    """Parses commandline arguments and runs EEGprep for the specified scope
    
    Args:
        args (Namespace, optional): Object with eeg prep parameters 
            as attributes. Defaults to None.
    """
    log = Log()
    args = args or parse_arguments()
    log.received_arguments(args)
    
    io = InputOutput(log, args.data_directory)
    pipeline = Pipeline(log, args.dry_run)

    subjects = io.get_subject_labels()
    if args.subject_index:
        subjects = [subjects[args.subject_index-1]]

    if args.subject_label:
        subjects = [args.subject_label]
    for subject_label in subjects:
        job = SubjectJob(
            io.for_(subject=subject_label),
            log.new_partial_log()
        )
        job.add_to(pipeline)
    pipeline.run()

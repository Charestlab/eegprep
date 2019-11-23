from eegprep.args import parse_arguments
from eegprep.pipeline import Pipeline
from eegprep.inputoutput import InputOutput
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
    if args.subject_index:     
        args.subject_label = io.get_subject_label_for_index(0)

    if args.subject_label:
        job = SubjectJob()
        job.add_to(pipeline)
    pipeline.run()

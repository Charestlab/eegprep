from argparse import ArgumentParser


def parse_arguments(args=None):
    """Parse commandline parameters
    
    Args:
        args (str, optional): String of arguments, for testing purposes only. 
            Defaults to None.
    
    Returns:
        Namespace: Object with parsed arguments as properties
    """
    parser = ArgumentParser()
    parser.add_argument('data_directory', type=str, nargs='?', default='/data',
        help='root data directory')
    subject = parser.add_mutually_exclusive_group()
    subject.add_argument('-s', '--subject-index', type=int,
        help='index of subject to work on, when sorted alphabetically')
    subject.add_argument('-l', '--subject-label', type=str,
        help='label of subject to work on')
    return parser.parse_args(args)

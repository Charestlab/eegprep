from mne.utils.misc import sizeof_fmt as hsize


class Log(object):

    def write(self, message):
        print(message)

    def new_partial_log(self):
        return self

    def received_arguments(self, args):
        m = 'Command arguments:\n\t'
        m += '\n\t'.join([f'{k}: {v}' for k, v in vars(args).items()])
        self.write(m)

    def found_subjects(self, subjects):
        listed = ', '.join(subjects)
        self.write(f'Found {len(subjects)} subjects: {listed}')

    def started_pipeline(self, jobs):
        m = f'Starting pipeline with {len(jobs)} jobs:\n'
        job_lines = [f'{j+1}: {job.describe()}' for j, job in enumerate(jobs)]
        m += '\n'.join(job_lines)
        self.write(m)

    def starting_job(self, job):
        self.write(f'Starting job: ' + job.describe())

    def cleaning_up_after_job(self, job):
        self.write(f'Cleaning up after job: ' + job.describe())

    def discovering_data(self):
        self.write('Discovering data..')

    def storing_object_in_memory(self, key, obj, size, total_size):
        self.write(
            f'Storing object ({hsize(size)}) '
            f'in memory store ({hsize(total_size)})'
        )

    def removing_object_from_memory(self, key, obj, size, total_size):
        self.write(
            f'Removing object ({hsize(size)}) '
            f'from memory ({hsize(total_size)})'
        )

    def writing_object(self, obj, fpath):
        self.write(f'Writing object to disk at {fpath}')

    # TODO: job can flush log after done:  log.flush(io) (io.write_text(log.xyz))
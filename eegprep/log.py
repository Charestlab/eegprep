

class Log(object):

    def write(self, message):
        print(message)

    def new_partial_log(self):
        return self

    def received_arguments(self, args):
        m = 'eegprep command arguments:\n\t'
        m += '\n\t'.join([f'{k}: {v}' for k, v in vars(args).items()])
        self.write(m)

    def found_subjects(self, subjects):
        listed = ', '.join(subjects)
        self.write(f'found {len(subjects)} subjects: {listed}')

    def discovering_data(self):
        self.write('discovering data..')


    # TODO: job can flush log after done:  log.flush(io) (io.write_text(log.xyz))


class Log(object):

    def new_partial_log(self):
        return self

    def received_arguments(self, args):
        pass

    # TODO: job can flush log after done:  log.flush(io) (io.write_text(log.xyz))
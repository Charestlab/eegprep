

class BaseJob(object):

    def __init__(self, io, log):
        self.io = io
        self.log = log

    def add_to(self, pipeline):
        pipeline.add(self)

    def run(self):
        raise NotImplementedError(self.__class__.__name__ + '.run()')

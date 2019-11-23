

class BaseJob(object):

    def __init__(self, io, log):
        self.io = io
        self.log = log

    def add_to(self, pipeline):
        raise NotImplementedError(self.__class__ + '.add_to()')

    def run(self):
        raise NotImplementedError(self.__class__ + '.run()')

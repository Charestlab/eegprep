

class BaseJob(object):

    def __init__(self, io, log):
        self.io = io
        self.log = log

    def describe(self):
        """Return a string that describes this job
        
        Returns:
            str: one-line string describing this job and it's scope
        """
        scope = self.io.describe_scope()
        return scope + ' ' + self.__class__.__name__.replace('Job', '')

    def add_to(self, pipeline):
        pipeline.add(self)

    def run(self):
        raise NotImplementedError(self.__class__.__name__ + '.run()')

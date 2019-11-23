
class Pipeline(object):

    def __init__(self, log, dry):
        self.log = log
        self.dry = dry
        self.jobs = []

    def add(self, job):
        self.jobs.append(job)

    def run(self):
        pass


class Pipeline(object):

    def __init__(self, log, dry):
        self.log = log
        self.dry = dry
        self.jobs = []

    def add(self, job):
        self.jobs.append(job)

    def run(self):
        self.log.started_pipeline(self.jobs)
        if self.dry:
            return
        for job in self.jobs:
            self.log.starting_job(job)
            job.run()

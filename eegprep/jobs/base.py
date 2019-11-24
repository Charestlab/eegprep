

class BaseJob(object):

    def __init__(self, io, log):
        self.io = io
        self.log = log
        self.jobs_to_expire = []

    def get_id(self):
        return self.__class__.__name__.replace('Job', '')

    def describe(self):
        """Return a string that describes this job
        
        Returns:
            str: one-line string describing this job and it's scope
        """
        scope = self.io.describe_scope()
        return scope + ' ' + self.get_id()

    def add_to(self, pipeline):
        self.add_children_to(pipeline)
        pipeline.add(self)

    def add_children_to(self, pipeline):
        pass

    def run(self):
        pass

    def cleanup(self):
        for job in self.jobs_to_expire:
            self.io.expire_output_of(job)

    def expire_output_on_cleanup(self, job):
        self.jobs_to_expire.append(job)

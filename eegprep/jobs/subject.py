from eegprep.jobs.base import BaseJob
from eegprep.jobs.run import RunJob
from eegprep.jobs.concat_epochs import ConcatEpochsJob


class SubjectJob(BaseJob):

    def add_to(self, pipeline):
        runs = self.io.get_run_labels()
        for run_label in runs:
            job = RunJob(self.io.for_(run=run_label))
            job.add_to(pipeline)
        if runs:
            job = ConcatEpochsJob(self.io)
            job.add_to(pipeline)

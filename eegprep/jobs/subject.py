from eegprep.jobs.base import BaseJob
from eegprep.jobs.run import RunJob
from eegprep.jobs.concat_epochs import ConcatEpochsJob


class SubjectJob(BaseJob):

    def add_children_to(self, pipeline):
        found_data = False
        sessions = self.io.get_session_labels()
        for session_label in sessions:
            session_io = self.io.for_(session=session_label)
            for run_label in session_io.get_run_labels():
                found_data = True
                job = RunJob(session_io.for_(run=run_label), self.log)
                job.add_to(pipeline)
                self.expire_output_on_cleanup(job)
        if found_data:
            job = ConcatEpochsJob(self.io, self.log)
            job.add_to(pipeline)

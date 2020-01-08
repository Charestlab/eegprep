from eegprep.jobs.base import BaseJob


class FilterJob(BaseJob):

    def run(self):
        raw = self.io.retrieve_object('raw')
        raw.filter(l_freq=0.05, h_freq=45, fir_design='firwin')
        self.io.store_object(raw, name='raw', job=self)

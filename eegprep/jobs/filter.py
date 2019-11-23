from eegprep.jobs.base import BaseJob


class FilterJob(BaseJob):

    def run(self):
        # Filtering
        raw = raw.filter(l_freq=0.05, h_freq=45, fir_design='firwin')

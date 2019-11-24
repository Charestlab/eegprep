from eegprep.jobs.base import BaseJob
from eegprep.jobs.read import ReadJob
from eegprep.jobs.filter import FilterJob
from eegprep.jobs.epoch import EpochJob


class RunJob(BaseJob):
    """Represents preprocessing of one raw data file.
    """

    def add_children_to(self, pipeline):
        job = ReadJob(self.io, self.log)
        job.add_to(pipeline)
        self.expire_output_on_cleanup(job)
        job = FilterJob(self.io, self.log)
        job.add_to(pipeline)
        self.expire_output_on_cleanup(job)
        job = EpochJob(self.io, self.log)
        job.add_to(pipeline)
        # io.store_output_of(job)

        # plot raw data
        # nchans = len(raw.ch_names)
        # pick_channels = numpy.arange(0, nchans, numpy.floor(nchans/20)).astype(int)
        # start = numpy.round(raw.times.max()/2)
        # fig = raw.plot(start=start, order=pick_channels)
        # fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_raw.png'.format(sub, ses, task, run)
        # fig.savefig(join(reportsdir, fname_plot))

        # # create evoked plots
        # conds = clean_epochs.event_id.keys()
        # selected_conds = random.sample(conds, min(len(conds), 6))
        # picks = mne.pick_types(clean_epochs.info, eeg=True)
        # for cond in selected_conds:
        #     evoked = clean_epochs[cond].average()
        #     fname_plot = 'sub-{}_ses-{}_task-{}_run-{}_evoked-{}.png'.format(sub, ses, task, run, cond)
        #     fig = evoked.plot_joint(picks=picks)
        #     fig.savefig(join(reportsdir, fname_plot))

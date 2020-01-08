import mne, pandas
from eegprep.jobs.base import BaseJob
from eegprep.guess import guess_montage


class ReadJob(BaseJob):

    def run(self):

        fpath_raw = self.io.get_filepath(suffix='eeg')
        ext = fpath_raw[-3:]
        raw_funcs = {
            'bdf': mne.io.read_raw_bdf,
            'edf': mne.io.read_raw_edf
        }
        raw = raw_funcs[ext](fpath_raw, preload=True, verbose=False)

        # Set channel types and select reference channels
        fpath_channels = self.io.get_filepath(suffix='channels')
        channels = pandas.read_csv(fpath_channels, index_col='name', sep='\t')
        bids2mne = {
            'MISC': 'misc',
            'EEG': 'eeg',
            'EOG': 'eog',
            'VEOG': 'eog',
            'TRIG': 'stim',
            'REF': 'eeg',
        }
        channels['mne'] = channels.type.replace(bids2mne)
        raw.set_channel_types(channels.mne.to_dict())

        # set bad channels
        # raw.info['bads'] = channels[channels.status=='bad'].index.tolist()

         # Set reference
        refChannels = channels[channels.type=='REF'].index.tolist()     
        raw.set_eeg_reference(ref_channels=refChannels) 
        # can now drop reference electrodes
        raw.set_channel_types({k: 'misc' for k in refChannels})

        # tell MNE about electrode locations
        montageName = guess_montage(raw.ch_names)
        montage = mne.channels.make_standard_montage(kind=montageName)
        raw.set_montage(montage, verbose=False)

        self.io.store_object(raw, name='raw', job=self)

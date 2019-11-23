from eegprep.jobs.base import BaseJob
# from os.path import join, basename
# import os, glob, random, numpy, mne, pandas
# from eegprep.guess import guess_montage


class ReadJob(BaseJob):

    def run(self):
                # read data
        raw = mne.io.read_raw_bdf(fpath, preload=True, verbose=False)

        # Set channel types and select reference channels
        channelFile = fpath.replace('eeg.bdf', 'channels.tsv') # maybe should be a string arg
        channels = pandas.read_csv(channelFile, index_col='name', sep='\t')
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




        # can now drop reference electrodes
        raw.set_channel_types({k: 'misc' for k in refChannels})

        # set bad channels
        # raw.info['bads'] = channels[channels.status=='bad'].index.tolist()

        # pick channels to use for epoching
        #epoching_picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, exclude='bads')

        montage = mne.channels.read_montage(guess_montage(raw.ch_names))
        # print(montage)
        raw = raw.set_montage(montage, verbose=False)


         # Set reference
        refChannels = channels[channels.type=='REF'].index.tolist()     
        raw = raw.set_eeg_reference(ref_channels=refChannels)
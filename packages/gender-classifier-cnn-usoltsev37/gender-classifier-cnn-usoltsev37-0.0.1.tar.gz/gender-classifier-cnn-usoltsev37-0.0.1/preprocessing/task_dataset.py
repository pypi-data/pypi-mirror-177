import random

import torch
import torchaudio
from torch.utils.data import Dataset


#
# Dataset for classification
#
class TaskDataset(Dataset):
    def __init__(self, df, data_path: str):
        self.df = df
        self.data_path = data_path
        self.max_seconds = 5
        self.sr = 24000

    #
    # Number of items in dataset
    # @return int
    #
    def __len__(self):
        return len(self.df)

    #
    # Get item from dataset by index
    #
    # @params
    #   idx - index of item in dataset
    # @return Tuple[spec, gender]
    #   spec - transforms.MelSpectrogram (shape=[1, 64, time_series])
    #   gender - target (0 or 1)
    #
    def __getitem__(self, idx):
        audio_file_path = self.data_path + self.df.loc[idx, 'PATH_TO_FILE']
        audio = torchaudio.load(audio_file_path)
        gender = self.df.loc[idx, 'GENDER']

        # Preprocessing
        dur_aud = self.crop_signal(audio, self.max_seconds)
        spec = self.create_db_spectrogram(dur_aud, n_mels=64, n_fft=1024, hop_len=512)

        return spec, gender

    #
    # Convert the signal to a fixed size 'max_seconds'
    #
    # @params
    #   'audio' - audio signal consists of (signal, sampling rate)
    #   'max_seconds'- fixed size of the signal
    # @return transforms.MelSpectrogram
    #
    def crop_signal(self, audio: tuple, max_seconds: int):
        sig, sr = audio
        max_width = sr * max_seconds
        sig_height, sig_width = sig.shape

        if sig_width > max_width:
            sig = sig[:, :max_width]
        elif sig_width < max_width:
            pad_start_width = random.randint(0, max_width - sig_width)
            pad_end_width = max_width - sig_width - pad_start_width
            sig = torch.cat((torch.zeros((sig_height, pad_start_width)),
                             sig,
                             torch.zeros((sig_height, pad_end_width))), 1)

        return sig, sr

    #
    # Create DB Spectrogram
    #
    # @params
    #   'audio' - audio signal consists of (signal, sampling rate)
    #   'n_mels' - number of mel filterbanks
    #   'n_fft' - size of FFT
    #   'hop_len' - length of hop between STFT windows
    # @return transforms.MelSpectrogram
    #
    def create_db_spectrogram(self, aud, n_mels=64, n_fft=1024, hop_len=None):
        sig, sr = aud
        spec = torchaudio.transforms.MelSpectrogram(sr, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(sig)
        spec = torchaudio.transforms.AmplitudeToDB(top_db=120)(spec)
        return spec

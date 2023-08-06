import pandas as pd
import torch

from preprocessing.task_dataset import TaskDataset


class DataLoader():

    def __init__(self, batch_size, shuffle):
        self.data_path = '/Users/thebest/Documents/HSE/semester_7/engineering-practices/hse-engineering-practices-ml/gender-classifier-cnn/'

        df_train = pd.read_csv(self.data_path + 'LibriTTS/train-dev-clean.csv', sep=';')
        ds_train = TaskDataset(df_train, self.data_path)
        self.dl_train = torch.utils.data.DataLoader(ds_train, batch_size=batch_size, shuffle=shuffle)

        df_test = pd.read_csv(self.data_path + 'LibriTTS/train-dev-clean.csv', sep=';')
        ds_test = TaskDataset(df_test, self.data_path)
        self.dl_test = torch.utils.data.DataLoader(ds_test, batch_size=batch_size, shuffle=shuffle)

        df_val = pd.read_csv(self.data_path + 'LibriTTS/train-dev-clean.csv', sep=';')
        df_val.head()
        ds_val = TaskDataset(df_val, self.data_path)
        self.dl_val = torch.utils.data.DataLoader(ds_val, batch_size=batch_size, shuffle=shuffle)

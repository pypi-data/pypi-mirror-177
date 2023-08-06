import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from tqdm import tqdm

from model.cnn import CNNClassifier


class Model():

    def __init__(self):
        self.model = CNNClassifier()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.is_fitted = False

    #
    # Train
    #
    def train(self, train_dl, val_dl, num_epochs, lr=0.001):
        # Loss Function, Optimizer and Scheduler
        CELoss = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=lr,
                                                        steps_per_epoch=int(len(train_dl)),
                                                        epochs=num_epochs,
                                                        anneal_strategy='linear')
        train_loses = []
        val_loses = []
        train_acc = []
        val_acc = []

        def plot_learning():
            plt.figure(figsize=(12, 6))
            plt.title('Loss')
            plt.plot(range(len(train_loses)), train_loses, label='train')
            plt.plot(range(len(val_loses)), val_loses, label='val')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            plt.tight_layout()
            plt.show()

            plt.figure(figsize=(12, 6))
            plt.title('Accuracy')
            plt.plot(range(len(train_acc)), train_acc, label='train')
            plt.plot(range(len(val_acc)), val_acc, label='val')
            plt.xlabel('Epoch')
            plt.ylabel('Acc')
            plt.legend()
            plt.tight_layout()
            plt.show()

        def run_epoch(is_validate: bool, dl, l_loses, l_acc, log_mode: str):
            running_loss = 0.0
            right_predictions = 0
            all_predictions = 0

            for i, data in enumerate(dl):
                inputs, labels = data[0].to(self.device), data[1].to(self.device)

                # Normalize because of BatchNorm layers in model
                inputs_m, inputs_s = inputs.mean(), inputs.std()
                inputs = (inputs - inputs_m) / inputs_s

                # Zero the parameter gradients
                if not is_validate:
                    optimizer.zero_grad()

                # forward
                outputs = self.model(inputs)
                loss = CELoss(outputs, labels)

                if not is_validate:
                    # backward + optimize
                    loss.backward()
                    optimizer.step()
                    scheduler.step()

                running_loss += loss.item()
                _, prediction = torch.max(outputs, 1)

                right_predictions += (prediction == labels).sum().item()
                all_predictions += prediction.shape[0]

            num_batches = len(dl)
            curr_loss = running_loss / num_batches
            accuracy = right_predictions / all_predictions
            l_loses.append(curr_loss)
            l_acc.append(accuracy)
            return f'{log_mode}: Epoch: {epoch}, Loss: {curr_loss:.2f}, Accuracy: {accuracy:.2f}'

        for epoch in tqdm(range(num_epochs)):
            log_train = run_epoch(is_validate=False, dl=train_dl, l_loses=train_loses, l_acc=train_acc,
                                  log_mode='TRAIN')
            with torch.no_grad():
                log_val = run_epoch(is_validate=True, dl=val_dl, l_loses=val_loses, l_acc=val_acc, log_mode='VAL')
            print('\t' + log_train)
            print(log_val)

        print('Finished Training')
        self.is_fitted = True
        plot_learning()

    #
    # Inference
    #
    def inference(self, dl):
        if not self.is_fitted:
            return
        right_predictions = 0
        all_predictions = 0
        true_positive = 0
        false_positive = 0
        false_negative = 0

        with torch.no_grad():
            for data in dl:
                inputs, labels = data[0].to(self.device), data[1].to(self.device)

                inputs_m, inputs_s = inputs.mean(), inputs.std()
                inputs = (inputs - inputs_m) / inputs_s

                outputs = self.model(inputs)
                _, prediction = torch.max(outputs, 1)

                true_positive += (np.logical_and(labels == True, prediction == True)).sum().item()
                false_positive += (np.logical_and(labels == False, prediction == True)).sum().item()
                false_negative += (np.logical_and(labels == True, prediction == False)).sum().item()
                right_predictions += (prediction == labels).sum().item()
                all_predictions += prediction.shape[0]

        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        accuracy = right_predictions / all_predictions

        print(f'Accuracy: {accuracy:.2f}, Total items: {all_predictions}')
        print(f'Precision: {precision}, Recall: {recall}')

    def state_dict(self):
        return self.model.state_dict()

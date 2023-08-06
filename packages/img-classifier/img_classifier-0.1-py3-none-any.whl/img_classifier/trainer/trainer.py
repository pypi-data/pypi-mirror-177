from argparse import Namespace
from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report
from torch.utils.data import DataLoader
from tqdm import tqdm

import wandb
from img_classifier.config import IMGCPath
from img_classifier.logger import get_logger
from img_classifier.utils import get_criterion, get_optimizer, get_scheduler

LOGGER = get_logger()


class IMGCTraner(IMGCPath):
    def __init__(
        self,
        config: Namespace,
        model: Callable,
        train_loader: DataLoader,
        valid_loader: DataLoader,
        device,
    ):
        super(IMGCTraner, self).__init__(config)
        self.model = model
        self.train_loader = train_loader
        self.valid_loader = valid_loader
        self.device = device
        self.criterion: Optional[Callable] = None
        self.optimizer: Optional[Callable] = None
        self.scheduler: Optional[Callable] = None

    def init_trainer(self):
        # 손실함수 초기화
        self.criterion = get_criterion(self.config)
        # 옵티마이저 초기화
        self.optimizer = get_optimizer(self.model, self.config)
        # 스케쥴러 초기화
        self.scheduler = get_scheduler(self.config.scheduler_type, self.optimizer, len(self.train_loader), self.config)

    def train_loop(self, epoch):
        self.model.train()

        train_perform = np.zeros(2)
        train_acc = 0

        pbar = tqdm(enumerate(self.train_loader), total=len(self.train_loader), position=0)

        for idx, value in pbar:
            pbar.set_description(f"EPOCH-{epoch}/{self.config.epochs}")
            image, labels = value
            image = image.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()

            output = self.model(image)

            loss = self.criterion(output, labels)
            loss.backward()
            self.optimizer.step()
            self.scheduler.step()

            predict = output.argmax(dim=-1)
            labels = labels.detach().cpu().numpy()
            predict = predict.detach().cpu().numpy()

            train_acc = accuracy_score(labels, predict)

            train_perform += np.array([loss.item(), train_acc])

            pbar.set_postfix(
                avg_loss=train_perform[0] / (idx + 1),
                avg_acc=train_perform[1] / (idx + 1),
            )
        print(
            f"[+] Epoch {epoch:#04d} loss: {train_perform[0] / len(self.train_loader):#.5f}, acc: {train_perform[1] / len(self.train_loader):#.2f}"
        )

        return train_perform

    def valid_loop(self):
        self.model.eval()

        valid_perform = np.zeros(2)

        all_valid_predict_lst = []
        all_valid_labels_lst = []

        valid_acc = 0

        with torch.no_grad():
            for value in self.valid_loader:
                image, valid_labels = value
                image = image.to(self.device)
                valid_labels = valid_labels.to(self.device)

                valid_output = self.model(image)

                valid_loss = self.criterion(valid_output, valid_labels)

                valid_predict = valid_output.argmax(dim=-1)
                valid_predict = valid_predict.detach().cpu().numpy()
                valid_labels = valid_labels.detach().cpu().numpy()

                valid_acc = accuracy_score(valid_labels, valid_predict)

                valid_perform += np.array([valid_loss.item(), valid_acc])

                # valid set 기준 예측값 리스트
                all_valid_predict_lst += list(valid_predict)

                # valid set 기준 GT 리스트
                all_valid_labels_lst += list(valid_labels)

            if self.config.is_valid_classification_report:
                report = classification_report(all_valid_labels_lst, all_valid_predict_lst)
                print(f'[+] Valid classification report \n {report}')

        return valid_perform, all_valid_predict_lst, all_valid_labels_lst

    def train(self):

        LOGGER.info("[+] Start training.")

        if self.config.is_wandb:
            wandb.login()

            wandb.init(
                project=self.config.wandb_project_name,
                name=self.config.wandb_exp_name,
                config=self.config,
            )

            wandb.watch(self.model, log="all")

        # train & valid perfrom 초기화
        train_perform = np.zeros(2)
        valid_perform = np.zeros(2)
        all_valid_predict_lst = []
        all_valid_labels_lst = []

        # 베스트 loss & accuracy 초기화
        best_val_loss = np.inf
        best_val_acc = 0

        # early stopping counter 초기화
        early_stopping_counter = 0

        for epoch in tqdm(range(1, self.config.epochs + 1)):

            # 모델 학습 모드
            train_perform = self.train_loop(epoch)
            # 모델 검증 모드
            valid_perform, all_valid_predict_lst, all_valid_labels_lst = self.valid_loop()

            train_total_loss = train_perform[0] / len(self.train_loader)
            train_total_acc = train_perform[1] / len(self.train_loader)

            val_total_loss = valid_perform[0] / len(self.valid_loader)
            val_total_acc = valid_perform[1] / len(self.valid_loader)

            if self.config.is_wandb:
                wandb.log(
                    {
                        "train_loss": train_total_loss,
                        "train_accuracy": train_total_acc,
                        "valid_loss": val_total_loss,
                        "valid_accuracy": val_total_acc,
                    }
                )

            best_val_loss = min(best_val_loss, val_total_loss)

            if val_total_acc > best_val_acc:
                LOGGER.info(f"[+] New best model for val accuracy : {val_total_acc:#.4f}! saving the best model..")
                self.save_model(self.model)

                best_val_acc = val_total_acc
                early_stopping_counter = 0

            else:
                early_stopping_counter += 1
                if early_stopping_counter >= self.config.patience:
                    LOGGER.info(f"[+] EarlyStopping counter: {early_stopping_counter} out of {self.config.patience}")

                    break

            LOGGER.info(f"[+] Final Validation loss: {val_total_loss:#.4f}, Acc: {val_total_acc:#.4f}")

    def save_model(self, model):
        LOGGER.info(f"[+] Saving model to : {self.save_model_file_path}")
        torch.save(model.state_dict(), str(self.save_model_file_path))

    def test(self):
        LOGGER.info("[+] Start testing.")

    def inference(self):
        LOGGER.info("[+] Start inference.")

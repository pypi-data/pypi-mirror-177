import os
import random

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam, AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from transformers import get_linear_schedule_with_warmup

from img_classifier.logger import get_logger
from img_classifier.loss.loss import FocalLoss, LabelSmoothingLoss
from img_classifier.optimizer.optimizer import AdamP
from img_classifier.scheduler.scheduler import CosineAnnealingWarmupRestarts

# from img_classifier.config import get_configuration_parser


LOGGER = get_logger()
# config = get_configuration_parser()


def seed_everything(seed: int):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    LOGGER.info(f"[+] Seed set as {seed}")


def get_criterion(config):
    if config.smoothing != 0 and config.criterion_type == "smoothing":
        criterion = LabelSmoothingLoss(smoothing=config.smoothing)
    elif config.criterion_type == "cross":
        criterion = nn.CrossEntropyLoss()
    elif config.criterion_type == "focal":
        criterion = FocalLoss(gamma=2.0)
    else:
        raise NotImplementedError("Criterion not available")
    return criterion


def get_optimizer(model, config):
    if config.optimizer_type == "adam":
        optimizer = Adam(model.parameters(), lr=config.lr, weight_decay=0.01)
    elif config.optimizer_type == "adamw":
        optimizer = AdamW(model.parameters(), lr=config.lr, weight_decay=0.01)
    elif config.optimizer_type == "adamp":
        optimizer = AdamP(
            model.parameters(),
            lr=config.lr,
            betas=(0.9, 0.999),
            weight_decay=0.01,
            delta=0.1,
            wd_ratio=0.1,
            nesterov=False,
        )
    else:
        raise NotImplementedError("Optimizer not available")

    return optimizer


def get_scheduler(scheduler_type, optimizer, total_batch_, config):
    if config.scheduler_type == "plateau":
        return ReduceLROnPlateau(optimizer, patience=4, factor=0.85, mode="max", verbose=True)

    elif config.scheduler_type == "linear":
        return get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=total_batch_ * 2,
            num_training_steps=int(total_batch_ * config.epochs),
        )

    elif scheduler_type == "cosine":
        # assert warmup_steps < first_cycle_steps
        return CosineAnnealingWarmupRestarts(
            optimizer,
            first_cycle_steps=300,
            warmup_steps=config.warmup_steps,
            cycle_mult=config.cycle_mult,
            max_lr=config.lr,
            min_lr=config.lr * 0.01,
            gamma=0.8,
        )
    else:
        raise NotImplementedError("Scheduler not available")

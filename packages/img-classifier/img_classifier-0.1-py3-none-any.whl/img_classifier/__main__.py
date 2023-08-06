import torch
from torchinfo import summary

from img_classifier.config import IMGCPath, get_configuration_parser
from img_classifier.dataloader.dataloader import get_data_loaders, get_datasets
from img_classifier.logger import get_logger
from img_classifier.model.model import get_model
from img_classifier.trainer.trainer import IMGCTraner
from img_classifier.utils import seed_everything

LOGGER = get_logger()

if __name__ == "__main__":
    config = get_configuration_parser()
    path = IMGCPath(config)

    seed_everything(config.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    LOGGER.info(f"[+] PROJECT NAME : {config.project_name}")
    LOGGER.info(f"[+] TASK : {config.task}")
    LOGGER.info(f"[+] MODE : {config.mode}")
    LOGGER.info(f"[+] {device} device is used")

    LOGGER.info(f"[+] Get Dataset")
    train_dataset, valid_dataset, dataset_classes = get_datasets(
        config.pretrained, str(path.raw_dataset_folder_path), config.split_ratio, config.resize
    )

    LOGGER.info("[+] Load Model")
    model = get_model(config.plm_model_name, config.pretrained, config.is_plm_weight_freeze, len(dataset_classes))
    total_params = sum(p.numel() for p in model.parameters())
    LOGGER.info(f"  [-] {total_params:,} total parameters.")
    total_trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    LOGGER.info(f"  [-] {total_trainable_params:,} training parameters.")
    summary(model)

    if config.mode == "train":
        train_loader, valid_loader = get_data_loaders(
            train_dataset, valid_dataset, config.batch_size, config.num_worker
        )
        model.to(device)
        trainer = IMGCTraner(config, model, train_loader, valid_loader, device)
        trainer.init_trainer()
        trainer.train()

    elif config.mode == "test":
        pass

    elif config.mode == "inference":
        pass

from argparse import ArgumentParser, Namespace
from pathlib import Path


def get_configuration_parser() -> Namespace:
    main_parser = ArgumentParser()

    main_parser.add_argument("--project_name", default="img_Classification", type=str)
    main_parser.add_argument("--task", default="classification", type=str)
    main_parser.add_argument("--mode", default="train", type=str, choices=["train", "test", "inference"])
    main_parser.add_argument("--seed", default=1004, type=int)
    main_parser.add_argument("--root_path", default="./img_classifier", type=str)
    main_parser.add_argument(
        "--plm_model_name",
        default="efficientnet",
        type=str,
        choices=[
            "efficientnet_b0",
            "efficientnet_b6",
            "resnet_50",
            "resnet_152",
            "vgg16_bn",
        ],
    )
    main_parser.add_argument("--train_file", default="train_5labels.csv", type=str)
    main_parser.add_argument("--raw_dataset_folder_path", default="data/Chess", type=str)
    main_parser.add_argument("--save_model_folder_path", default="save_model", type=str)
    main_parser.add_argument("--save_model_file_name", default="model.pt", type=str)

    model_parser = main_parser.add_argument_group("model")
    model_parser.add_argument("--num_classes", default=5, type=int)
    model_parser.add_argument(
        "--pretrained",
        default=True,
        type=lambda s: s.lower() in ["true", 1],
        help="Whether to use pretrained weights or not",
    )
    model_parser.add_argument(
        "--is_plm_weight_freeze",
        default=True,
        type=lambda s: s.lower() in ["true", 1],
        help="whether to freeze pretrained weight or not",
    )

    dataset_parser = main_parser.add_argument_group("dataset")
    dataset_parser.add_argument("--split_ratio", default=0.2, type=float)

    transform_parser = main_parser.add_argument_group("transform")
    transform_parser.add_argument("--resize", default=224, type=int)

    dataloader_parser = main_parser.add_argument_group("dataloader")
    dataloader_parser.add_argument("--num_worker", default=4, type=int)

    trainer_parser = main_parser.add_argument_group("trainer")
    trainer_parser.add_argument("--epochs", default=20, type=int)
    trainer_parser.add_argument("--batch_size", default=64, type=int)
    trainer_parser.add_argument("--lr", default=1e-4, type=float)
    trainer_parser.add_argument("--smoothing", default=0.0, type=float)
    trainer_parser.add_argument("--criterion_type", default="cross", type=str, choices=["cross", "smoothing", "focal"])
    trainer_parser.add_argument("--optimizer_type", default="adamw", type=str, choices=["adam", "adamw", "adamp"])
    trainer_parser.add_argument("--scheduler_type", default="linear", type=str)
    trainer_parser.add_argument("--warmup_steps", default=500, type=int)
    trainer_parser.add_argument("--cycle_mult", default=1.2, type=float)
    trainer_parser.add_argument("--patience", default=5, type=int)
    trainer_parser.add_argument(
        "--is_valid_classification_report", default=True, type=lambda s: s.lower() in ["true", 1]
    )

    wandb_parser = main_parser.add_argument_group("wandb")
    wandb_parser.add_argument("--is_wandb", default=True, type=lambda s: s.lower() in ["true", 1])
    wandb_parser.add_argument("--wandb_project_name", default="img_classification", type=str)
    wandb_parser.add_argument("--wandb_exp_name", default="draft", type=str)

    return main_parser.parse_args()


class IMGCPath:
    def __init__(self, config: Namespace):
        self.config = config
        self.root_path = Path(self.config.root_path)
        self.setup_directory()

    def setup_directory(self):
        self.raw_dataset_folder_path.mkdir(parents=True, exist_ok=True)
        self.save_model_folder_path.mkdir(parents=True, exist_ok=True)

    @property
    def raw_dataset_folder_path(self) -> Path:
        return self.root_path / self.config.raw_dataset_folder_path

    @property
    def save_model_folder_path(self) -> Path:
        return self.root_path / self.config.save_model_folder_path

    @property
    def save_model_file_path(self) -> Path:
        return self.save_model_folder_path / self.config.save_model_file_name

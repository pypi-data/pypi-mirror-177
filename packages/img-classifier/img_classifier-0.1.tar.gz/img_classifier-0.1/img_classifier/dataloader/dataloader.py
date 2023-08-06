import torch
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


# Training transforms
def get_train_transform(image_size, pretrained):
    train_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.GaussianBlur(kernel_size=(5, 9), sigma=(0.1, 5)),
            transforms.RandomAdjustSharpness(sharpness_factor=2, p=0.5),
            transforms.ToTensor(),
            normalize_transform(pretrained),
        ]
    )
    return train_transform


# Validation transforms
def get_valid_transform(image_size, pretrained):
    valid_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            normalize_transform(pretrained),
        ]
    )
    return valid_transform


# Image normalization transforms.
def normalize_transform(pretrained):
    if pretrained:  # Normalization for pre-trained weights.
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    else:  # Normalization when training from scratch.
        normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    return normalize


def get_datasets(pretrained, dataset_file_path, split_ratio, image_size):
    dataset = datasets.ImageFolder(
        dataset_file_path, transform=(get_train_transform(image_size, pretrained))
    )
    dataset_test = datasets.ImageFolder(
        dataset_file_path, transform=(get_valid_transform(image_size, pretrained))
    )
    dataset_size = len(dataset)

    # Calculate the validation dataset size.
    valid_size = int(split_ratio * dataset_size)
    # Radomize the data indices.
    indices = torch.randperm(len(dataset)).tolist()
    # Training and validation sets.
    dataset_train = Subset(dataset, indices[:-valid_size])
    dataset_valid = Subset(dataset_test, indices[-valid_size:])

    return dataset_train, dataset_valid, dataset.classes


def get_data_loaders(dataset_train, dataset_valid, batch_size, num_workers):
    train_loader = DataLoader(
        dataset_train, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    valid_loader = DataLoader(
        dataset_valid, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    return train_loader, valid_loader

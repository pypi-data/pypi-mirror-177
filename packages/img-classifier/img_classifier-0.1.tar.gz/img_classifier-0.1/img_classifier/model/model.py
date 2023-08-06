import ssl
import warnings

import torch.nn as nn
import torchvision.models as models

from img_classifier.logger import get_logger

warnings.filterwarnings("ignore", category=UserWarning)

ssl._create_default_https_context = ssl._create_unverified_context


LOGGER = get_logger()


def get_model(
    plm_model_name: str,
    pretrained: bool,
    is_plm_weight_freeze: bool,
    num_classes: int,
):
    if plm_model_name == "efficientnet_b0":
        if pretrained:
            LOGGER.info("[+] Loading pre-trained weights")
        else:
            LOGGER.info("[+] Not loading pre-trained weights")
        model = models.efficientnet_b0(pretrained=pretrained)

        if is_plm_weight_freeze:
            LOGGER.info("[+] Freezing hidden layers...")
            for params in model.parameters():
                params.requires_grad = False
        elif not is_plm_weight_freeze:
            LOGGER.info("[+] Fine-tuning all layers...")
            for params in model.parameters():
                params.requires_grad = True

        # Change the final classification head.
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features=in_features, out_features=num_classes)
        return model

    elif plm_model_name == "efficientnet_b6":
        if pretrained:
            LOGGER.info("[+] Loading pre-trained weights")
        else:
            LOGGER.info("[+] Not loading pre-trained weights")
        model = models.efficientnet_b6(pretrained=pretrained)

        if is_plm_weight_freeze:
            LOGGER.info("[+] Freezing hidden layers...")
            for params in model.parameters():
                params.requires_grad = False
        elif not is_plm_weight_freeze:
            LOGGER.info("[+] Fine-tuning all layers...")
            for params in model.parameters():
                params.requires_grad = True

        # Change the final classification head.
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features=in_features, out_features=num_classes)
        return model

    elif plm_model_name == "resnet_50":
        if pretrained:
            LOGGER.info("[+] Loading pre-trained weights")
        else:
            LOGGER.info("[+] Not loading pre-trained weights")
        model = models.resnet50(pretrained=pretrained)

        if is_plm_weight_freeze:
            LOGGER.info("[+] Freezing hidden layers...")
            for params in model.parameters():
                params.requires_grad = False
        elif not is_plm_weight_freeze:
            LOGGER.info("[+] Fine-tuning all layers...")
            for params in model.parameters():
                params.requires_grad = True

        # Change the final classification head.
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features=in_features, out_features=num_classes)
        return model

    elif plm_model_name == "resnet_152":
        if pretrained:
            LOGGER.info("[+] Loading pre-trained weights")
        else:
            LOGGER.info("[+] Not loading pre-trained weights")
        model = models.resnet152(pretrained=pretrained)

        if is_plm_weight_freeze:
            LOGGER.info("[+] Freezing hidden layers...")
            for params in model.parameters():
                params.requires_grad = False
        elif not is_plm_weight_freeze:
            LOGGER.info("[+] Fine-tuning all layers...")
            for params in model.parameters():
                params.requires_grad = True

        # Change the final classification head.
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features=in_features, out_features=num_classes)
        return model

    elif plm_model_name == "vgg16_bn":
        if pretrained:
            LOGGER.info("[+] Loading pre-trained weights")
        else:
            LOGGER.info("[+] Not loading pre-trained weights")
        model = models.vgg16_bn(pretrained=pretrained)

        if is_plm_weight_freeze:
            LOGGER.info("[+] Freezing hidden layers...")
            for params in model.parameters():
                params.requires_grad = False
        elif not is_plm_weight_freeze:
            LOGGER.info("[+] Fine-tuning all layers...")
            for params in model.parameters():
                params.requires_grad = True

        # Change the final classification head.
        num_features = model.classifier[6].in_features
        features = list(model.classifier.children())[:-1]
        features.extend([nn.Linear(num_features, num_classes)])
        model.classifier = nn.Sequential(*features)
        return model

    else:
        raise NotImplementedError("not available plm_model name, insert correct plm_model name")

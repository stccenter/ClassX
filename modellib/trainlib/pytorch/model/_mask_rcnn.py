"""Module to create the Mask-RCNN Model Instance"""
# Python Third Party Imports
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
import torchvision


__all__ = ['create_mask_rcnn_model']

def create_mask_rcnn_model(num_classes:int=2,
                           hidden_layers:int=256,
                           mode:str="evaulation",
                           model_path:str=None,
                           device:torch.device=None):
    """Function to create the mask-rcnn model object in pytorch

    Args:
        num_classes (int, optional): The number of classes for the
        research field. Defaults to 2.
        hidden_layers (int, optional): _description_. Defaults to 256.
        mode (str, optional): The mode to load the model in, options are "train" or "evaluation".
        model_path (str, optional): The path to the model state last used.
        device (str, optional): The device to use for running the model. Defaults to "cpu".

    Returns:
        torchvision.model: The Mask-RCNN Model Object
    """
    print("Num Classes:", num_classes)
    # Getting the model
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(num_classes=num_classes)

    # Replacing features classes to update it with current version.
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features , num_classes)
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                       hidden_layers,
                                                       num_classes)
    # Loading previous model state
    if model_path is not None:
        model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))

    # Loading the device to utilize for model. Defaults to cpu if none available.
    if device == None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Loading model onto device
    model.to(device)

    if mode == "train":
        model.train()
    elif mode == "evaluation" or "eval":
        model.eval()
    else:
        raise NotImplementedError("Mode selected is unavailable or unimplemented for Mask-RCNN Model")

    # NOTE When loading a model the settings need to be the same as
    # when it was trained or errors will occur

    # Returning the model object
    return model

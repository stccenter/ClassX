# Python Standard Library Imports

# Python Third Party Imports
import torch
import torchvision.transforms.v2 as T
import numpy as np

# Local Library Imports
from .model import create_mask_rcnn_model
class PytorchModel():
    def __init__(self,
                 model_path:str,
                 model_name:str,
                 num_classes:int,
                 device=None):
        self.model_path = model_path
        self.model_name = model_name
        self.num_classes = num_classes
        self.device = device
        self.model = self._load_pytorch_model()

    def _load_pytorch_model(self):
        # Loading pytorch model based off name
        if self.model_name == "mask-rcnn":
            model = create_mask_rcnn_model(model_path=self.model_path,
                                           num_classes=self.num_classes,
                                           device=self.device,
                                           mode="evaluation")
        return model

    def run_prediction(self, image) -> np.ndarray:
        # transform = T.Compose([
        #     T.ToImage()])
        transform = T.ToTensor()
        image = image[:,:,0]
        #print(image)
        image_transform = transform(image)
        with torch.no_grad():
            prediction = self.model([image_transform.to(self.device)])
        try:
            print(prediction)
            mask = np.zeros((image.shape[:2]), dtype=np.float32)
            if len(prediction[0]["masks"])  != 0:
                #original_mask = (prediction[0]["masks"][0].cpu().detach().numpy()[0,:,:])
                labels = prediction[0]["labels"]
                for prediction_index in range(len(prediction[0]["masks"])):
                    temp_mask = (prediction[0]["masks"][prediction_index].cpu().detach().numpy())
                    
                    mask = np.where(temp_mask[0,:,:] > np.max(temp_mask)/2, prediction_index+1, mask)
            #print(len(prediction[0]["masks"]))
        except Exception as error:
            print(error)
            print("ERROR")
            print(len(prediction[0]["masks"]))
            mask = np.zeros(image.shape[:2])
        return mask

class PytorchModelLoader():
    """Python class to load and categorize Pytorch models
    Attributes:
        model_dict (dict): Dictionary for accessing the different models based off
        their research field id.
    """

    def __init__(self):
        # Initializing an empty dict for the models
        self.model_dict = {}

        # Setting the device for the loader based off system.
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def set_model(self,
                  model_id:int,
                  model_name:int,
                  model_path:str,
                  num_classes:int
                  ) -> PytorchModel:
        """Function to set the model of a specific research field based off their id.

        Args:
            model_id (int): The research id from the database object
            model_name (int): The name of the model to load.
            model_path (str): The path of the model to load the state dict from.
            label_map (str): Label map for formatting returns afterwards.
        """
        # Loading the model object
        model_obj = self._load_model(model_name, model_path, num_classes)

        # Checking if the research field was already initialized with another model
        if model_id not in self.model_dict.keys():
            self.model_dict[model_id] = {}
        # Setting the model by it's name and research field id
        self.model_dict[model_id][model_name] = model_obj

    def get_model(self, model_id:int, model_name:str):
        "Getter function to retrieve a model for a research field"
        try:
            return self.model_dict[model_id][model_name]
        except KeyError:
            return None

    def _load_model(self,
                    model_name:str,
                    model_path:str,
                    num_classes:int):
        """Function to load and initialze a model object into memory.

        Args:
            model_name (str): The name of the model to load
            model_path (str): Path to the model state file.
            label_map (dict): Map of labels for processing image returns.
        """
        model_obj = PytorchModel(model_path=model_path,
                                 model_name=model_name,
                                 num_classes=num_classes,
                                 device=self.device)
        return model_obj


# Python Standard Library Imports
import traceback
import ast
import json
import os

# Python Third Party Imports
from flask import Blueprint, jsonify, make_response, redirect, request, url_for
from flask import Flask
import numpy as np

# Local Library Imports
from trainlib.pytorch.PytorchModelLoader import PytorchModelLoader
model_loader = PytorchModelLoader()

# Initializing the Flask Application
app = Flask(__name__)

# Initializing the Model Class.


def merge_directory(base_dir: str, sub_dir: str = "") -> str:
    """Joins two file paths together in a cross-platform manner.

    Args:
        base_dir (str): Base directory to join together.
        sub_dir (str): Sub directory or file name to join with base.

    Raises:
        ValueError: If either base_dir or sub_dir is not a string.

    Returns:
        str: A combined file path.
    """
    # Verifying the function arguments
    if not isinstance(base_dir, str) or not isinstance(sub_dir, str):
        raise ValueError("Both base_dir and sub_dir must be strings.")

    # Returns the directory in the correct OS format
    return os.path.join(base_dir, sub_dir).replace("\\", "/").rstrip("/")


def read_json(directory: str, encoding: str = "utf-8") -> dict:
    """Reads Json files and returns them as dictionaries

    Args:
        directory (str): Directory path to json file
        encoding (str, optional): Encoding used when reading
        json file. Defaults to "utf-8".

    Raises:
        TypeError: If directory is not a string
        TypeError: If encoding is not a string

    Returns:
        dict: Dictionary of json file structure
    """
    try:
        # Verifying the arguments
        if not isinstance(directory, str):
            raise TypeError("TypeError: directory argument must be of type string")

        if not isinstance(encoding, str):
            raise TypeError("TypeError: encoding key needs to be of type string")

        # Verifying the file existance
        if os.path.isfile(directory):
            # Opening the json file as read only
            with open(directory, "r", encoding="utf-8") as json_file:
                # Loading the json data
                directory = json.load(json_file)

                # Closing the Json File
                # json_file.close()
            return directory
        else:
            print("Error: File not found in directory:",directory)
            return None
    except (TypeError, OSError,
            FileNotFoundError) as error:
        print("Failed to read Json File")
        print(error)
        traceback.print_tb(error.__traceback__)
        return None


@app.route('/')
def home():
    return "This is a dummy flask app for mask-rcnn test inside the proper directory"

@app.route("/process_image/", methods=["GET","POST"])
def process_image():
    """
    API ENDPOINT
    Api for loading and running the detection results for the Mask-RCNN Model.
    """
    #try:
    # Receiving the request data
    request_data = request.get_json()
    #print("Request Data")
    #print(request_data)
    # Reshaping the image and converting back to numpy array
    image_string = ast.literal_eval(request_data["image"])
    image = np.frombuffer(image_string, dtype=np.float32).reshape(request_data["image_shape"])
    image = np.copy(image)
    # Loading the correct model based off the research ID
    model = model_loader.get_model(model_id=request_data["model_id"], model_name="mask-rcnn")
    if model is None:
        # If model is None means first load hasn't happened yet.
        model_file = read_json("./modellib/model_dir.json")
        #print(request_data["num_classes"])
        model_info = model_file[str(request_data["model_id"])]
        
        model_path = merge_directory("./modellib/trained_models",model_info["directory"])
        model_loader.set_model(model_id=request_data["model_id"],
                               model_name="mask-rcnn",
                               model_path=model_path,
                               num_classes=request_data["num_classes"])
        model = model_loader.get_model(model_id=request_data["model_id"],model_name="mask-rcnn")
    segment_image = model.run_prediction(image)
    response = {"image_shape":segment_image.shape,
                "segment_image":str(segment_image.tobytes())}
    return jsonify(response)
    #return render_template("dashboard.html")
    # except Exception as e:
    #     print(e)
    #     traceback.print_tb(e.__traceback__)
    #     return make_response(("", 500, {"error": "Failed to run model"}))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
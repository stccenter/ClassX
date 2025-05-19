"""Validates the name, style, and type of a given upload file"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
from werkzeug.utils import secure_filename

# Local Library Imports
from ..database.service import OriginalImageService

__all__ = ['validate_upload_files']

def validate_upload_files(file_upload_list:list,
                          user_id:int,
                          domain_data_protocol:dict,
                          original_image_service:OriginalImageService) -> dict:
    """Validates the name, style, and type of a given upload file

    Files can be sorted into 3 different types: valid, invalid, and duplicate.
    Valid:
        Means the file passed all check and will be uploaded successfully.
    Invalid:
        Means the file failed to pass a check that
        deemed in unsuitable to be uploaded.
    Duplicate:
        Means the file already exists in the system.

    Args:
        file_upload_list (list): The files to be uploaded.
        user_id (int): The user's id for which the user is attempting to upload.
        original_image_service (OriginalImageService): The class that connects to
        the database's original image table.
        domain_data_protocol (dict): The "protocol" which we use to determine if the file is valid.
    Raises:
        TypeError: If user_id is not an int
        TypeError: If original_image_service is not the correct class type
        TypeError: If the domain protocol is not a dict

    Returns:
        file_list(dict): A dictionary containing the files that were
        sorted into valid, invalid, or duplicate
    """
    if not isinstance(domain_data_protocol, dict):
        raise TypeError("TypeError: Domain protocol must be of type dict")

    # Declaring the dict that will be returned
    file_list = {"validated":[],"duplicate":[],"invalid":[]}
    try:
        for file in file_upload_list:
            # Get file name
            upload_file_name = secure_filename(file.filename)
            if len(upload_file_name) > 120:
                print("Invalid File detected : %s", upload_file_name)
                file_list["invalid"].append(upload_file_name)
                continue

            # # Check if file already exists in database
            if original_image_service.check_duplicate_user_image(user_id,upload_file_name) is True:
                print("Existing File Detected : %s", upload_file_name)
                file_list["duplicate"].append(upload_file_name)
                continue

            # Ensure the file is valid and can be added
            if upload_file_name.endswith(domain_data_protocol["file_type"]) is False:
                print("Invalid File detected : %s", upload_file_name)
                file_list["invalid"].append(upload_file_name)
                continue

            # Validate and upload file
            # Check if there is existing criteria to validate with
            if domain_data_protocol["fields"] is None or "None":
                print("File Validated : %s", upload_file_name)
                file_list["validated"].append(file)

            # Begin checking and validating the file
            else:
                # Get validation criteria
                validation_fields = domain_data_protocol["fields"]
                # Split portions of the file name based off the split character criteria
                file_name_fields = upload_file_name.removesuffix(domain_data_protocol["file_type"])
                file_name_fields = file_name_fields.split(validation_fields["split"])

                # Check if the beginning of the file's name matches what's expected
                if file_name_fields[0] != domain_data_protocol["file_head"]:
                    print("Invalid File detected : %s", upload_file_name)
                    file_list["invalid"].append(upload_file_name)
                    continue
                # Iterate based off the number of fields that need to be checked
                for field in range(validation_fields["num_fields"]):
                    print("Field being checked: %s & Existing field: %s", field, validation_fields)
                    field_info = validation_fields[str(field+1)]

                    # Check if the number of fields found is the same
                    # if check_file_field(file_name_fields[field+1],
                    #                     field_info["content"],
                    #                     field_info["length"]) is False:
                    #     print("Invalid File detected : %s", upload_file_name)
                    #     file_list["invalid"].append(upload_file_name)
                    #     break
                else:
                    # Finally validate the file NOT the name of the file
                    print("Validating File : %s", upload_file_name)
                    file_list["validated"].append(file)
        print("Validation Complete")
        return file_list
    except (TypeError, ValueError, RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return {"validated":[],"duplicate":[],"invalid":[]}

def check_file_field(field:str, field_type:str, field_length:int=0) -> bool:
    """Function to check the validity of a certain section within a file name

    Args:
        field (str): The field or section of the file to check
        field_type (str): The type of validation to perform
        field_length (int): length of the field

    Raises:
        ValueError: If the field provided is not a string
        TypeError: If the field type keyword is not a string keyword.
        ValueError: If the length provided is not a integer

    Returns:
        bool: returns True or False based off if the field passed validation
    """
    #Validating arguments
    if not isinstance(field, str):
        raise ValueError("ValueError: Field must of type string")
    if not isinstance(field_type, str):
        raise TypeError("TypeError: field type must be submitted as a string")
    if not isinstance(field_length, int):
        raise ValueError("ValueError: field length must of of type int")
    try:

        # Check if the number of fields found is the same
        if len(field) != field_length and field_length != 0:
            return False
        # Check that content fields are correct
        if field_type == "digit" and field.isdigit() is False:
            return False
        # Check that character fields contain strictly A-Z characters
        if field_type == "letter" and field.isalpha() is False:
            return False
        return True
    except (TypeError, ValueError, RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return False

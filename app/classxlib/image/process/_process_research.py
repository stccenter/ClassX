# Python Third Party Imports
from skimage.exposure import histogram
from skimage.feature import peak_local_max

# Local Library Imports
from ...database.model import ResearchField, OriginalImage
from .._write import write_cv_image, write_hdf5_image
from ._icebridge import _process_icebridge_image
from ._heliophysics import _process_heliophysic_image
from ...file import format_image_directories, format_database_path

__all__ = ['process_research_image']

def process_research_image(image_path:str,
                         image_savepath:str,
                         file_name:str,
                         research_field_obj:ResearchField):
    """Takes an image filepath from a default research field and processes it. Function requires the research field
    to be one of the default supported research fields.

    Args:
        image_filepath (str): The file path to open the image from.
        processed_image_save_path (str): Where the image should be saved after processing.
        file_name (str): File name for image to be saved under.
        research_field_obj (ResearchField) : Database research field object used for processing the image.

    Raises:
        TypeError: If the image file path is not of type String
        TypeError: If the image save path is not of type String
        TypeError: If the file name is not of type String
        TypeError: If the research_field_obj is the incorrect class object.
        Exception: If the research field object is not a default research field.

    Returns:
        tuple: _description_
    """
    #Verifying Arguments
    if not isinstance(image_path, str):
        raise TypeError("TypeError: directory argument must be of type string")
    if not isinstance(image_savepath, str):
        raise TypeError("TypeError: directory argument must be of type string")
    if not isinstance(file_name, str):
        raise TypeError("TypeError: file_name argument must be of type string")
    if not isinstance(research_field_obj, ResearchField):
        raise TypeError("TypeError: Incorrect Class object for research_field_obj")
    #Checking if the research_field is default
    #If type is equal to 1 that means it's a default research_field.
    if research_field_obj.visibility == 1:
        return _process_default_image(image_path=image_path,
                               image_savepath=image_savepath,
                               file_name=file_name,
                               research_field_obj=research_field_obj)


def _process_default_image(image_path:str,
                           image_savepath:str,
                           file_name:str,
                           research_field_obj:ResearchField):
    # Processing image based off which default supported domain it is
    if research_field_obj.name == "Arctic Ice":
        image_data_dict, image_dim, creation_date, metadata_dict = _process_icebridge_image(image_path, research_field_obj)
        image_savepath_dict = format_image_directories(dir_=image_savepath,
                                                       file_name=file_name,
                                                       file_head="DMS",
                                                       file_type=".tif")

    elif research_field_obj.name == "Heliophysics":
        image_data_dict, image_dim, creation_date, metadata_dict = _process_heliophysic_image(image_path, research_field_obj)
        image_savepath_dict = format_image_directories(dir_=image_savepath,
                                                       file_name=file_name,
                                                       file_head="aia",
                                                       file_type=".fits")
    else:
        return None
    write_cv_image(image_data_dict['visual'],image_savepath_dict['visual'])
    write_hdf5_image(image_data_dict['h5'],image_savepath_dict['h5'])
    write_cv_image(image_data_dict['thumbnail'],image_savepath_dict['thumbnail'])
    write_cv_image(image_data_dict['grid'],image_savepath_dict['grid'])

    image_db_path_dict = {}
    image_db_path_dict['visual'] = format_database_path(image_savepath_dict['visual'])
    image_db_path_dict['h5'] = format_database_path(image_savepath_dict['h5'])
    image_db_path_dict['thumbnail'] = format_database_path(image_savepath_dict['thumbnail'])
    image_db_path_dict['grid'] = format_database_path(image_savepath_dict['grid'])

    return image_db_path_dict, image_dim, creation_date, metadata_dict

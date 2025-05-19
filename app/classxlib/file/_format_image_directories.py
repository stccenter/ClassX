"""Module to create the file save paths for processed images"""

# Python Standard Library Imports
import traceback

# Local Library Import
from ._manage_directory import merge_directory

__all__ = ['format_image_directories']

def format_image_directories(dir_: str,
                             file_name:str,
                             file_head:str,
                             file_type:str) -> dict:
    """Creates file save paths for processed images

    Args:
        dir_ (str): Directory to save in
        file_name (str): File name to format
        file_head (str): File header to change name of
        file_type (str): Type of file saving

    Raises:
        TypeError: If the dir_ is not of type string
        TypeError: If the file_name is not of type string
        TypeError: If the file_head is not of type string

    Returns:
        dict: Formatted dict object with all the savepaths
        {`"visual"`:Save path for the visualization image,
         `"h5"`:Save path for the normalized
         image data saved in hdf5 files,
         `"thumbnail"`:Save path for the thumbnail image,
         `"grid"`: Save path for the grid image}
    """
    try:
        if not isinstance(dir_, str):
            raise TypeError("TypeError: directory argument must be of type string")
        if not isinstance(file_name, str):
            raise TypeError("TypeError: file_name argument must be of type string")
        if not isinstance(file_head, str):
            raise TypeError("TypeError: file_head argument must be of type string")

        # Save path for the visualization image
        visual_image_savepath = merge_directory(dir_, file_name.replace(file_type,
                                                                        ".png"))

        # Save path for the normalized image data
        h5_savepath = visual_image_savepath.replace(file_head,
                                                    ("h5_"+file_head))
        h5_savepath = h5_savepath.replace(".png",".h5")

        # Save path for the thumbail image
        thumbnail_savepath = visual_image_savepath.replace(file_head,
                                                           ("thumbnail_"+file_head))

        # Save path for the image with gridlines drawn
        grid_savepath = visual_image_savepath.replace(file_head,
                                                      ("grid_"+file_head))

        # Dictionary to return all paths in
        file_path_dict = {"visual":visual_image_savepath,
                          "h5":h5_savepath,
                          "thumbnail":thumbnail_savepath,
                          "grid":grid_savepath}
        return file_path_dict
    except (ValueError, TypeError,
            RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return {}

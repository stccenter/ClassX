"""Processing module for processing segmentation
parameters"""

# Python Standard Library Imports
import traceback

__all__ = ['process_segment_parameters']

def process_segment_parameters(parameter_data:list)-> dict:
    """A layer separation function meant to convert segment
    parameter data sent from front-end into a readable format
    also changes key names to be easier to understand

    Args:
        parameter_data (list): The parameter data sent from front-end

    Returns:
        dict: Formatted dictionary with all settings processed
    """
    try:
        parameter_dict = {}
        request_dict = {}
        for parameter in parameter_data:
            request_dict[parameter['name']] = parameter['value']

        # NOTE Any used settings are generally set to 0 this is for
        # purposes of saving in the database afterwards since 0
        # indicates an unused parameter

        # ID of Cropped Image
        parameter_dict['crop_image_id'] = int(request_dict['id'])

        # This is a confirmation check from front-end to dismiss warnings
        if request_dict.keys().__contains__("confirm"):
            parameter_dict['confirm'] = int(request_dict['confirm'])

        ### Segmentation Algorithm Parameters ###
        # Segment Algorithm Method ID
        # 1: Watershed
        # 2: SLIC
        # 3: Felzenswalb
        # 4: Quickshift
        # Each ID references which algorithm to use
        parameter_dict['segment_method_id'] = int(request_dict['menu'])
        parameter_dict['parameter_1'] = float(request_dict['param1'])
        parameter_dict['parameter_2'] = float(request_dict['param2'])
        parameter_dict['parameter_3'] = float(request_dict['param3'])

        # Watershed algorithm doesn't use a second parameter so set it to zero
        if parameter_dict['segment_method_id'] == 1:
            parameter_dict['parameter_2'] = 0

        ### Pre-Processing Parameters ###

        # Light Adjustment Parameters
        # Check if we should generate additonal previews with lighting adjusted
        parameter_dict['light_adjustment_check'] = int(request_dict['LightAdjustmentCheck'])

        # This is only returned on the save API call not the preview
        # We check to see if it exists because of this
        if request_dict.keys().__contains__("hist_method"):
            parameter_dict['histogram_method'] = int(request_dict['hist_method'])
        else:
            parameter_dict['histogram_method'] = 0

        # Contrast Stretch Parameter
        parameter_dict['contrast_stretch_check'] = int(request_dict['ContrastStretchCheck'])

        # Color Quantization Parameters
        parameter_dict['color_cluster_check'] = int(request_dict['ColorClustCheck'])
        parameter_dict['color_cluster_method'] = int(request_dict['menuColor'])
        parameter_dict['color_clusters'] = int(request_dict['Color_Clusters0'])

        # Checking if it was enabled or not
        if parameter_dict['color_cluster_check'] == 0:
            parameter_dict['color_cluster_method'] = 0
            parameter_dict['color_clusters'] = 0

        # Multiprocessing parameter
        parameter_dict['multi_processing_check'] = int(request_dict['multiProcessingCheck'])

        ### Post-Processing Parameters ###

        # Region Merging Parameters
        parameter_dict['region_merge_check'] = int(request_dict['RAGCheck'])
        parameter_dict['region_merge_method'] = int(request_dict['menuRAG'])
        parameter_dict['region_merge_threshold'] = float(request_dict['RAG_Threshold0'])
        # Checking to see if it was enabled or not
        if parameter_dict['region_merge_check'] == 0:
            parameter_dict['region_merge_method'] = 0
            parameter_dict['region_merge_threshold'] = 0
        # Method 2 doesn't use a threshold so we set it to zero
        if parameter_dict['region_merge_method'] == 2:
            parameter_dict['region_merge_method'] = int(request_dict['menuRAG'])
            parameter_dict['region_merge_threshold'] = 0

        # Small Feature Removal Parameters
        parameter_dict['small_item_removal_check'] = int(request_dict['small_rem'])
        parameter_dict['small_item_removal_threshold'] = int(request_dict['rem_threshold'])
        if parameter_dict['small_item_removal_check'] == 0:
            parameter_dict['small_item_removal_threshold'] = 0

        return parameter_dict
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("Failure Processing Segmentation Settings")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None

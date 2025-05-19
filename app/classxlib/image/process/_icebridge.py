"""Module for processing the DMS Tiff images retrieved from the NASA Icebridge Portal"""

# Python Standard Library Imports
from datetime import datetime

# Python Third Party Imports
import numpy as np
from skimage.exposure import histogram
from skimage.feature import peak_local_max

# Local Library Imports
from ...database.model import ResearchField
from ...image.utils import get_channel, set_channel
from .._read import read_geotiff_image
from ..transform import rescale_intensity, crop_rotate_image, resize_image
from ..analysis import get_image_light
from ...utils import parse_float
from ..process import process_image_grid

__all__ = ['_process_icebridge_image']

def _process_icebridge_image(path:str, research_field_obj:ResearchField):
    """Function for processing the DMS tiff images from the Nasa Icebridge
    Mission"""

    # This the WGS 84 coordinate system text to provide for converting coordinates
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""

    # Reading the tiff image into memory and extracting metadata and coordinates
    (image_data, image_metadata, image_coordinates) = read_geotiff_image(path=path,
                                                                  reverse_axis=True,
                                                                  return_coordinate=True,
                                                                  coordinate_system=wgs84_wkt)
    # Cropping out the black background and rotating the image
    image_data = crop_rotate_image(image_data)

    # Processing the image data for use
    image_data = _color_balance_image(image_data)

    # Getting the light value of the image
    light_value = get_image_light(np.copy(image_data),
                                 data_range=(0,255))

    # Processing the image metadata
    metadata_dict, creation_date = _process_metadata(image_metadata=image_metadata,
                                                    image_coordinates=image_coordinates,
                                                    image_light_value=light_value)

    # Dimensions of image
    image_dim = (image_data.shape[1],image_data.shape[0])

    image_data_dict = {}

    # Creating a copy for the visual image
    image_data_dict['visual'] = np.copy(image_data)

    # Making the original adjusted data
    image_data_dict['h5'] = rescale_intensity(image_data,
                                                old_range=(0,255),
                                                new_range=(0.0, 1.0))

    # Creating the thumbnail image
    image_data_dict['thumbnail'] = resize_image(input_image=image_data_dict['visual'],
                                                vertical_scale=int(image_dim[1]*0.1),
                                                horizontal_scale=int(image_dim[0]*0.1))
    # Getting the crop size for the auto grid
    crop_size = research_field_obj.protocols['auto_grid_size']

    # Creating the grid image
    image_data_dict['grid'] = process_image_grid(input_image=image_data_dict['visual'],
                                                 crop_size=crop_size)

    return image_data_dict, image_dim, creation_date ,metadata_dict


def _color_balance_image(input_image:np.ndarray,channel_axis:int=None):
    """Balances the colors in an arctic tif image

    Args:
        input_image (np.ndarray): Numpy array of the image
        channel_axis (int, optional): Channel axis where the image. Defaults to None.
    """
    # Checking for the channel axis to use on the image
    if channel_axis is None:
        channel_axis = -1
    # The amount of color bands/channels on the image
    band_count = input_image.shape[channel_axis]

    # Looping through each band in the image
    for band_index in range(band_count):
        # Retrieving the color channel from the image
        band_data = get_channel(input_image=input_image,
                                channel=band_index,
                                channel_axis=channel_axis)
        # Getting the band minimum and maximum
        band_min = np.min(band_data)
        band_max = np.max(band_data)

        # Number of intervals/bins
        nbins = int(band_max - band_min)

        # Histogram of the band
        band_histogram, bin_centers = histogram(band_data, nbins)

        # Getting the peaks within the image
        peaks = peak_local_max(band_histogram[1:],
                               exclude_border=False,
                               min_distance=5,
                               num_peaks=3,
                               threshold_abs=int(np.sum(band_histogram[0])*.004))

        # Getting the lower and upper ranges
        lower, upper = _find_threshold(band_histogram,
                                        bin_centers=bin_centers,
                                        peaks=peaks,
                                        src_dtype=8)

        # If there is only one peak we need to make sure the upper limit is correct
        if len(peaks) < 2 and upper < band_max * 0.8:
            upper = band_max * 0.8

        # Getting a mask where to equalize the image on
        mask = np.where(band_data > 0,
                        True,
                        False)

        # Clipping the band data to the lower and upper ranges
        band_data = np.clip(band_data,
                            a_min=lower,
                            a_max=upper,
                            where=mask)

        # Rescaling the band data
        band_data = rescale_intensity(band_data,
                                      old_range=(lower,upper),
                                      new_range=(1,255),
                                      target_dtype=np.uint8,
                                      mask=mask)

        # Applying the rescaled data to the original image
        set_channel(image=input_image,
                    new_channel_data=band_data,
                    chan=band_index,
                    channel_axis=channel_axis)
    return input_image

# pylint: disable=too-many-arguments too-many-locals
def _find_threshold(hist, bin_centers, peaks, src_dtype, top=0.15, bottom=0.5):
    """
    Finds the upper and lower threshold for
    histogram stretching.
    Using the indices of the highest and lowest peak
    (by intensity, not # of pixels), this searches for an upper
    threshold that is both greater than the highest
    peak and has fewer than 15% the number of pixels, and a lower
    threshold that is both less than the lowest peak
    and has fewer than 50% the number of pixels.
    10% and 50% picked empirically to give good results.
    """
    max_peak = np.max(peaks)  # Max intensity
    thresh_top = max_peak
    while hist[thresh_top] > hist[max_peak] * top:
        thresh_top += 1  # Upper limit is less sensitive, so step 2 at a time
        # In the case that the top peak is already at/near the max bit value, limit the top
        #   threshold to be the top bin of the histogram.
        if thresh_top >= len(hist)-1:
            thresh_top = len(hist)-1
            break

    min_peak = np.min(peaks)  # Min intensity
    thresh_bot = min_peak
    while hist[thresh_bot] > hist[min_peak] * bottom:
        thresh_bot -= 1
        # Similar to above, limit the bottom threshold to the lowest histogram bin.
        if thresh_bot <= 0:
            thresh_bot = 0
            break

    # Convert the histogram bin index to an intensity value
    lower = bin_centers[thresh_bot]
    upper = bin_centers[thresh_top]

    # Save the upper value for the auto white balance function
    # auto_wb = upper
    # Save the lower value for the black point reference
    # auto_bpr = lower

    # Determine the width of the lower peak.
    lower_width = min_peak - thresh_bot
    dynamic_range = max_peak - min_peak

    # Limit the amount of stretch to a percentage of the total dynamic range
    #   in the case that all three main surface types are not represented (fewer
    #   than 3 peaks)
    # 8 bit vs 11 bit (WorldView)
    # 256   or 2048
    # While WV images are 11bit, white ice tends to be ~600-800 intensity
    # Provide a floor to the amount of stretch allowed
    if src_dtype > 8:
        max_bit = 2047
    else:
        max_bit = 255

    # If the width of the lowest peak is less than 3% of the bit depth,
    #   then the lower peak is likely open water. 3% determined visually, but
    #   ocean has a much narrower peak than ponds or ice.
    if (float(lower_width)/max_bit >= 0.03) or (dynamic_range < max_bit / 3):
        min_range = int(max_bit * .08)
        lower = min(lower, min_range)

    # return lower, upper, auto_wb, auto_bpr
    return lower, upper

def _process_metadata(image_metadata, image_coordinates, image_light_value):
    """Proceses the metadata retrieved from the DMS image
    """
    # Assigning a type depending on brightness
    if image_light_value > 0.627:
        light = 'bright'
    elif image_light_value > 0.392:
        light = 'medium'
    else:
        light = 'poor'

    # Dictionary for metadata
    metadata_dict = {'light':light,
                     'longitude':float(image_coordinates[1]),
                     'latitude':float(image_coordinates[0]),
                     'altitude':parse_float(image_metadata['Altitude']),
                     'fstop':parse_float(image_metadata['FStop']),
                     'pitch':parse_float(image_metadata['Pitch']),
                     'roll':parse_float(image_metadata['Roll']),
                     'shutter_speed':parse_float(image_metadata['ShutterSpeed'])}

    # Date and time the image was taken
    gpsdatetime = datetime.strptime(image_metadata['GPSDate']
                                    + " "
                                    + image_metadata['GPSTime'][0:8],
                                    '%Y-%m-%d %H:%M:%S')

    return metadata_dict, gpsdatetime

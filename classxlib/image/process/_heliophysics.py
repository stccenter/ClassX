# Python Standard Library Imports
import copy

# Python Third Party Imports
import numpy as np
import matplotlib
from skimage.transform import resize

# Local Library Imports
from ...database.model import ResearchField
from .._read import read_fits_image
from ..transform import rescale_intensity, resize_image
from ..process import process_image_grid

# pylint: disable=invalid-name

__all__ = ["_process_heliophysic_image"]


def _process_heliophysic_image(path: str, research_field_obj: ResearchField):
    image_data, image_header, image_map = read_fits_image(path=path, index=1)
    processed_data, im_size, sun_radius, sun_center = _resize_EUV(
        image_data, image_header, 2
    )
    print("Resized Heliophyisc EUV")
    processed_data = _correct_limb_brightening(processed_data, sun_center, sun_radius)
    print("Corrected Limb Brightening")
    metadata_dict, creation_date = _process_metadata(image_map)
    # Dimensions of image
    image_dim = (processed_data.shape[1], processed_data.shape[0])

    image_data_dict = {}
    print("Processing visual image")
    # Creating a copy for the visual image
    image_data_dict["visual"] = _process_visual_image(image_data, image_dim)
    print("Processing h5 image")
    # Making the original adjusted data
    image_data_dict["h5"] = rescale_intensity(
        processed_data,
        old_range=(np.min(processed_data), np.max(processed_data)),
        new_range=(0.0, 1.0),
    )
    print("Processing thumbnail image")
    # Creating the thumbnail image
    image_data_dict["thumbnail"] = resize_image(
        input_image=image_data_dict["visual"],
        vertical_scale=int(image_dim[1] * 0.1),
        horizontal_scale=int(image_dim[0] * 0.1),
    )

    # Getting the crop size for the auto grid
    crop_size = research_field_obj.protocols["auto_grid_size"]

    print("Processing grid image")
    # Creating the grid image
    image_data_dict["grid"] = process_image_grid(
        input_image=image_data_dict["visual"], crop_size=crop_size
    )

    return image_data_dict, image_dim, creation_date, metadata_dict


def _process_visual_image(input_image: np.ndarray, image_dim: tuple):
    sdoaia171 = matplotlib.colormaps["sdoaia171"]
    input_image = np.log10(np.clip(input_image, 10, 16000, dtype=np.float32))
    input_image = (input_image - np.min(input_image)) / (
        np.max(input_image) - np.min(input_image)
    )
    input_image = np.uint8(sdoaia171(input_image) * 255)
    input_image = resize_image(
        input_image=input_image,
        vertical_scale=int(image_dim[1]),
        horizontal_scale=int(image_dim[0]),
    )
    return input_image


def _process_metadata(image_map):
    creation_date = image_map.date.datetime
    metadata_dict = {
        "longitude": float(image_map.carrington_longitude.deg),
        "latitude": float(image_map.carrington_latitude.deg),
        "measurement": float(image_map.measurement.value),
        "wavelength": float(image_map.wavelength.value),
        "exposure_time": float(image_map.exposure_time.value),
        "sun_distance": float(image_map.dsun.value),
    }

    return metadata_dict, creation_date


def _resize_EUV(J, h, resize_param=8, interpolation="Bi-cubic"):
    """
    Resizes solar EUV image based on user-specified resize parameter, and
    return useful metadata about resized image.

    Parameters
    ----------
    J : [float]
        Solar EUV image
    h : dict
        original .fits header
    resize_param : int
        Resize Parameter which defines the degree to which the image should be
        spatially downsampled. Note that the parameter can be interpreted as
        the denominator of a fraction such that a value of '2' would indicate
        that the output image should be 1/2 the original spatial resolution
        in each dimension, 4 indicates 1/4 scale, etc. By convention, this
        parameter is 8 for SDO-AIA images and 4 for STEREO A and STEREO B
        images, this produces an output that is 512x512 pixels in size.
    interpolation : str, optional
        Interpolation method for the resizing process. Valid options are
        'Nearest-neighbor','Bi-linear','Bi-quadratic','Bi-cubic',
        'Bi-quartic', and 'Bi-quintic'.

        Default Value: 'Bi-cubic'
    Returns
    -------
        I : [float]
            Solar EUV Image, resized to user-specified dimensions.
        im_size : [int]
            Array with provides the dimensions of the image.
        sun_radius : float
            Radius of the Sun in the resized image.
        sun_center : [int]
            Coordinates of the center of the sun in the resized image.
    """

    # Determine Downsample Method
    downsample = [
        "Nearest-neighbor",
        "Bi-linear",
        "Bi-quadratic",
        "Bi-cubic",
        "Bi-quartic",
        "Bi-quintic",
    ]
    for order in range(len(downsample)):
        if downsample[order] == interpolation:
            break

    # Resize image
    if resize_param > 1:
        I = resize(
            J,
            np.asarray(J.shape) / resize_param,
            order=order,
            preserve_range=True,
            anti_aliasing=True,
        )
    else:
        I = copy.deepcopy(J)

    # Determine characteristics of image
    im_size = np.asarray(I.shape)  # size of the image

    # Get Solar Radius from Metadata
    try:  # SDO/AIA
        sun_radius = h["R_SUN"] / resize_param
    except:  # STERO A or B
        sun_radius = (h["RSUN"] / h["CDELT1"]) / resize_param

    # Get Solar Center from Metadata
    sun_center = np.asarray([int(round(h["CRPIX1"])) - 1, int(round(h["CRPIX2"])) - 1])
    sun_center = sun_center / resize_param

    # Return Resized Image, Image Dimensions and Solar Radius & Center
    return I, im_size, sun_radius, sun_center


def _mask_circle_mask(c, im_dims, r):
    # defomes a binary image with image dimensions im_dims of a circle with
    # center c and radius r
    cx = c[0]
    cy = c[1]
    ix = im_dims[0]
    iy = im_dims[1]
    x, y = np.meshgrid(np.arange(-(cx), (ix - cx), 1), np.arange(-(cy), (iy - cy), 1))
    c_mask = (x**2 + y**2) <= r**2
    return c_mask


def _correct_limb_brightening(I, sun_center, sun_radius):
    im_size = np.asarray(I.shape)
    # make solar disk masks for the different regions of correction per [1]
    sd_mask = _mask_circle_mask(sun_center, im_size, sun_radius)
    r1, r2, r3, r4 = 0.7, 0.95, 1.08, 1.12
    sd_mask1 = _mask_circle_mask(sun_center, im_size, sun_radius * r1)
    sd_mask2 = _mask_circle_mask(sun_center, im_size, sun_radius * r2)
    sd_mask3 = _mask_circle_mask(sun_center, im_size, sun_radius * r3)
    sd_mask4 = _mask_circle_mask(sun_center, im_size, sun_radius * r4)

    # compute average intensity within each annulus of 1 pixel wide
    F = np.zeros(im_size)
    for r in np.arange(r1 * sun_radius, r4 * sun_radius, 1):
        annulus1 = _mask_circle_mask(sun_center, im_size, r)
        annulus2 = _mask_circle_mask(sun_center, im_size, r + 1)
        annulus = (annulus2 ^ annulus1) > 0
        F[annulus] = (annulus * I).sum() / annulus.sum()
    # define corrected image per [1]
    I_corr = np.zeros(im_size)
    I_corr[F > 0] = np.median(I[sd_mask]) * I[F > 0] / F[F > 0]

    # define smoothed corrected image
    I_smooth = np.zeros(im_size)
    # no correction for r<r1 or r>r4
    I_smooth[sd_mask1] = I[sd_mask1]
    I_smooth[~sd_mask4] = I[~sd_mask4]

    # complete correction for r2<r<r3
    region = (sd_mask3 ^ sd_mask2) > 0
    I_smooth[region] = I_corr[region]

    # smoothed correction for r1<r<r2
    for r in np.arange(r1 * sun_radius, r2 * sun_radius, 1):
        annulus1 = _mask_circle_mask(sun_center, im_size, r)
        annulus2 = _mask_circle_mask(sun_center, im_size, r + 1)
        annulus = (annulus2 ^ annulus1) > 0
        f = 0.5 * np.sin(np.pi / (r2 - r1) * (r / sun_radius - (r1 + r2) / 2)) + 0.5
        I_smooth[annulus] = (1 - f) * I[annulus] + f * I_corr[annulus]

    # smoothed correction for r3<r<r4
    for r in np.arange(r3 * sun_radius, r4 * sun_radius, 1):
        annulus1 = _mask_circle_mask(sun_center, im_size, r)
        annulus2 = _mask_circle_mask(sun_center, im_size, r + 1)
        annulus = (annulus2 ^ annulus1) > 0
        f = 0.5 * np.sin(np.pi / (r4 - r3) * (r / sun_radius + (r4 - 3 * r3) / 2)) + 0.5
        I_smooth[annulus] = (1 - f) * I[annulus] + f * I_corr[annulus]
    return I_smooth

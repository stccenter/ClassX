import React, { useEffect, useState } from 'react';
import { Anchor } from 'antd';
import { useOutletContext } from "react-router-dom";
import { dashboard, image_preview, Originaldms, HistEqualDMs, AdapEqualDms, CLAHEdms,
     kmean4, labelPage, login, registration, segmentedit, upload, view_labelcrop, viewFiles, 
     cropped_image_library, edit_name, image_cropping, new_name_alias, segmentation_navbar, 
     select_cropped_image_library, select_dashboard, adap4, kmean1, kmean2, kmean3, cropimageplacement, 
     ImagePanleDisplay, canvasimagep, SegmentationLabel, SegmentationTab, Segmentation_dropdown, 
     PP_revealTab, Seg_hover, crop_hover, MarkBoundariesbt, lightadjustmetnpre, AutoCropSwitch, 
     AutoGridePage, GridSelection, Iconbar, Piecharticon, BargraphIcob, ImageViewIcon, ButtonAutoLabel, 
     AutoLabelbar, Savefile_dropdown, Savebuttonlabel, savefilemodal, savefiledropdown, Savelabelconfo, 
     view_and_share_button, viewbutton, viewlabelcropdisplay, imagepreviewvie_and_share, shareIcon, shareodaloptions, Share_confo } from '../../assets/help_page_image';
import styled from "@emotion/styled"
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb';

const handleClick = (e: any, link: any) => {
    e.preventDefault();
    console.log(link);
};

// Assuming the breadcrumb is an array of objects with a name string.
interface BreadcrumbItem {
    name: string;
}

interface HelpContext {
    breadcrumb: BreadcrumbItem[];
    setBreadcrumb: (breadcrumb: BreadcrumbItem[]) => void;
}


const Help: React.FC = () => {
    //@ts-ignore
    const [breadcrumb, setBreadcrumb] = useOutletContext<HelpContext>()
    const [mainHeight, setMainHeight] = useState("100%")

    useEffect(() => {
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Help" }]))
        setMainHeight("90%")
    }, [])
    return (
        <div style={{ height: mainHeight, display: "flex" }}>
            <Document className="main" >
                <h2>User Guide for ClassX Labeling Tool</h2>
                <h3>ClassX (CX) Labeling Tool</h3>
                <h3><i>Image Labeling Service</i></h3>
                <h5>Version 0.5</h5>
                <h5>NSF Spatiotemporal Innovation Center</h5>

                <br />

                {/* Start introduction */}
                <section id="introDiv">
                    <h3>Introduction and Background</h3>
                    <a href='#anchor-demo-basic' />
                    <br />
                    <p>
                        The polar regions have become increasingly important as they provide significant potential natural resources and function as a key driver of the Earth's climate,
                        a sensitive indicator to human activities and global, environment, and climate changes. High spatial resolution (HSR) imagery is critical in Arctic sea ice
                        research for verifying the Earth observation satellite data, extracting sea ice physical parameters, and calibrating/validating climate models. However, these
                        images are discrete in space and time, in big volume, and are often not included in the existing Arctic data centers. To better understand, utilize, and protect
                        the polar regions, our team has developed:
                    </p>
                    <ol>
                        <br />
                        <li>
                            a cloud computing-based Arctic cyberinfrastructure (ClassX) to collect, search,
                            explore, visualize, organize, analyze and share the HSR images which are discrete in time and
                            space;
                        </li>
                        <li>
                            a prototype of an online service for sea ice images domain scientists can use to classify
                            image and extract geophysical parameters.
                        </li>
                    </ol>
                    <br />
                    <p>
                        The developed ClassX is an ideal platform for integrating existing time-series images. Specifically, the functionalities of ClassX include image data management,
                        user management, batch image processing, results review, and spatiotemporal visualization modules. We invite the scientific community to help test and evaluate this new
                        platform and to provide professional reviews, comments, and demands. This session is a hands-on guide on how to use the ClassX science gateway service to process
                        images for sea ice labeling. Arctic Cyberinfrastructure (ClassX) Labeling tool is an operational image labeling web-based tool for sea ice research that incorporates features such as:
                    </p>
                    <br />
                    <ol>
                        <li>  Image Segmentation</li>
                        <li>  Image labeling</li>
                        <li>  Visualization</li>
                        <li>  Sharing</li>
                        <li>  Integrating an efficient image segmentation functionality in the tool to automatically extract homogenous regions from the images</li>
                        <li>  Expanding the web-based tool to support solar studies</li>
                    </ol>
                </section>
                {/* End Introduction */}

                {/* Start Architecture */}
                <section id="archiDiv">
                    <br />
                    <h3> Downloading Data from the Operation IceBridge Portal</h3>
                    <br />
                    <iframe width="560" height="315" src="https://www.youtube.com/embed/-ADhwCBu3vA" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowFullScreen></iframe>
                    <br />
                </section>

                <br />
                {/* End Architecture */}

                <section id="userRegAndVer">
                    <br />
                    <h3 id="userReg">
                        <li>User Registration and Verification </li></h3>

                    <p>
                        Navigate to <a href="https://classx.stcenter.net/">ClassX portal</a> and sign in with your
                        account credentials. If you do not have an account, you can create one by following these steps:
                    </p>
                    <br />
                    <p>
                        First, click 'Register' below the credentials field or navigate to the <a href="https://classx.stcenter.net/keycloak/realms/STC-ClassX/login-actions/registration?client_id=flask-app&tab_id=LQPTDrDjfPY">Registration page.</a>
                    </p>
                    <br />
                    <img src={login} alt="ClassX Login" className="center" />
                    <br />
                    <p>
                        Next, enter your preferred account credentials in the corresponding text fields (First & Last Name, Username, Email, and
                        Password) and then click 'Register'
                    </p>
                    <br />
                    <img src={registration} alt="ClassX Register" className="center" />
                    <br />
                    <p>
                        The user is authorized in the JWT Token, authenticating the user.
                        By default, you are given various pre-supplied images to explore the applications and services offered.
                    </p>
                    <br />
                    <img src={dashboard} alt="Email Verification" className="center" />
                </section>

                <section id="profileMan">
                    <br />
                    <h3 id="profileManage">Image Exploration</h3>

                    <section id="vAndEprofile">
                        <br />
                        <h4><u>Image Search & Filter</u></h4>
                        <br />
                        <p>
                            Welcome to the Image Exploration section of our platform! Here, you can harness the power of powerful
                            search and filtering functionalities to refine your image exploration based on a variety of criteria.
                            This section will guide you through the process of efficiently finding and accessing the images that
                            best suit your research needs.
                        </p>

                        <br />

                        <p><b>Search Images:</b></p>

                        <p>1. To search for images by their name, simply enter the DMS image name into the search input box.</p>
                        <p>2. After entering the image name, click the "Search" button to find the
                            specific image you are looking for.
                        </p>

                        <p><b>Filter Images:</b></p>
                        <p>
                            1. Go to the "Filter" column to access advanced filtering options. This allows
                            you to filter images based on brightness, acquisition date, and uploader.
                        </p>
                        <p>
                            2. Use the filtering options to refine your search based on essential metadata attributes, such as
                            longitude, latitude, altitude, F-stop, roll, and shutter speed.
                        </p>
                        <p>
                            3. After selecting the desired filters, click the "Apply" button at the bottom of the column
                            to apply them and instantly view the filtered results.
                        </p>


                        <p>
                            <b>Clear Filters/Search:</b>
                        </p>
                        <p>
                            1. To clear the applied filters and search criteria, click the "Clear" button to reset them.
                        </p>
                        <p>
                            <b>Image Preview:</b>
                        </p>
                        <p>
                            When you click on a DMS image from the index page table, you will be able to view a full preview of the selected image.
                        </p>
                        <br />
                        <img src={image_preview} alt="Image Preview" className="center" />
                        <br />
                        <p>
                            With these advanced filtering capabilities, you can easily pinpoint and retrieve the images that align precisely with
                            your research goals. The site's integrated filtering mechanism ensures a seamless and productive user experience,
                            empowering researchers with the tools they need to extract valuable insights from our extensive image collection.
                        </p>
                    </section>

                    <section id="AliasImage">
                        <br />
                        <h4><u>Image Alias</u></h4>
                        <br />
                        <p>
                            The Image Alias feature allows you to customize the display name of a TIFF image on the index page. To set an alias for an image, follow these steps:
                        </p>
                        <p>
                            1. Click the Dashboard button next to the image whose name you wish to change.
                        </p>
                        <br />
                        <img src={select_dashboard} alt="Select Dashboard" className="center" />
                        <br />
                        <p>
                            2. In the Dashboard interface next to the name of an image is an edit icon, select that icon.
                        </p>
                        <br />
                        <img src={edit_name} alt="Edit Alias" className="center" />
                        <br />
                        <p>
                            3. Enter the desired alias in the input box that appears.
                        </p>
                        <br />
                        <img src={new_name_alias} style={{ height: "100x", width: "300px" }} alt="Save Icon" className="center" />
                        <br />
                        <p>
                            4. Click "OK" when prompted to save the alias. The new alias will now replace the original DMS name of the image.
                        </p>
                        <p>
                            5. If you leave the input box empty and click "OK", the alias will be reset to the DMS name.
                        </p>
                        <br />
                        <p>
                            By using the Image Alias functionality, you can personalize the image names to be more descriptive or recognizable, making it easier for you and other users to identify and work with specific images in the index page. This feature provides a convenient way to manage and reference your images according to your preferences.
                        </p>
                        <br />
                    </section>
                </section>

                <section id="ImageCrop">
                    <br />
                    <h3 id="ImageCrop">Image Crop</h3>
                    <section id="imagesearch">
                        <br />
                        <h4><u>Multi-Image Upload</u></h4>
                        <br />
                        <p>
                            <b>Overview</b>
                        </p>
                        <p>
                            The Multi-Image Upload functionality enables users to upload their own TIFF images for visualization, cropping, segmentation,
                            and labeling within the ClassX system. To upload images, simply click the "Upload Images" button, and a file explorer window will pop up,
                            allowing you to select up to 5 DMS TIFF images at once.

                            Please note that the current system version only accepts TIFF images from the IceBridge DMS L1B Geolocated and
                            Orthorectified Images dataset, which includes Level-1B imagery captured by the Digital Mapping System (DMS)
                            over Greenland and Antarctica. Additionally, the current training model accepts imagery taken over the ocean during
                            the spring period in Arctic regions. Ensure that the images you are uploading meet these requirements to avoid any errors.
                        </p>

                        <p>
                            After successful upload, you will receive a confirmation message (as shown in the image below), and your newly
                            uploaded files will appear at the top of the queue. Information such as the date and time of upload, your ClassX
                            username, image size. image light, dimensions, and spatial resolutions will be displayed for each uploaded image.
                        </p>
                        <br />
                        <p>
                            <b>Steps to Upload Images:</b>
                        </p>
                        <p>
                            1. Click the "Upload Images" button.
                        </p>
                        <p>
                            2. In the file explorer window, select up to 5 desired images.
                        </p>
                        <p>
                            3. Click "Open" to transfer the selected images to ClassX.
                        </p>
                        <br />
                        <img src={upload} alt="Image Upload" className="center" />
                    </section>

                    <section id="sendEmail">
                        <br />
                        <h4><u>Image Cropping</u></h4>
                        <br />
                        <p>
                            <b>Overview</b>
                        </p>
                        <br />
                        <p>
                            To crop a specific image, click on the 'Crop Image' button on the index page. This will take you to the cropping
                            page as shown below, where you can visualize the selected image along with the file name displayed at the top.
                            On the right side, you will see a real-time preview of the section chosen for cropping.

                            Additionally, we now provide an 'Auto Crop' option, which allows the system to automatically identify and crop
                            relevant regions within the image. You can access this option under the Image Segmentation page.

                            The cropping page also includes a table with functionalities and pointers to different areas of the image, making
                            the cropping process more intuitive and user-friendly.
                        </p>
                        <p>
                            Once you have chosen the dimensions and coordinates of the image to be cropped, click the 'Crop Image' button.
                            The system will provide a confirmation message upon successful cropping or notify you if any issues arise during the process.
                            After receiving the confirmation, you can proceed to the Image Segmentation process by clicking 'Image Segmentation'
                            in the header, which will lead you to the next section with a detailed description.
                        </p>
                        <br />
                        <img src={image_cropping} alt="Cropping Tool" className="center" />

                        <div id="accesslevelinfo" >
                            <br />
                            <table className="custom-table">
                                <thead>
                                    <tr>
                                        <th scope="col">Functionality</th>
                                        <th scope="col">Purpose</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td >Zoom Value Slider</td>
                                        <td >Allows you to change the zoom value (i.e., the dimension of the image to be cropped) by sliding along the slider.</td>
                                    </tr>
                                    <tr>
                                        <td >Box Pointer</td>
                                        <td >Indicates the area that will be cropped. The box pointer changes its outline color according to the Zoom Value. The box pointer stays blue when the Zoom value is 256. If the decided zoom value is less than 256, the box pointer will change to Red color. Similarly, if the zoom value is greater than 256, the box pointer turns green.</td>
                                    </tr>
                                    <tr>
                                        <td>Y and X Slider</td>
                                        <td>Allows you to change the y and x coordinate values of your box pointer either by sliding the slider or by clicking specific places where you would like to crop.</td>
                                    </tr>
                                    <tr>
                                        <td>Default Button</td>
                                        <td>Located below the Y-Slider, it resets your zoom value to 256, i.e., the default option.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <br />
                        <p>
                            <b>Steps to Crop the Image</b>
                        </p>
                        <p>
                            1. Click the "Crop Image" button on the Index page to access the cropping page.
                        </p>
                        <p>
                            2. Choose the dimensions and coordinates for the image to be cropped using the available sliders and pointers.
                        </p>
                        <p>
                            3. Click "Crop Image" to complete the cropping process.
                        </p>
                        <br />

                        <p>
                            <b>Cropped Image Library</b>
                        </p>
                        <p>
                            To view every cropped image you've made of the original image, follow these steps:
                        </p>
                        <p>
                            1. Select the Dashboard button for whichever image you want to see the cropped images for
                        </p>
                        <p>
                            2. Click on Cropped Image Library on the left hand side of the Dashboard interface.
                        </p>
                        <br />
                        <img src={select_cropped_image_library} alt="Select Cropped Image Library" className="center" />
                        <br />
                        <p>
                            3. From this screen you can select previous cropped images to segment, delete from the library, or create more crops of the image.
                        </p>
                        <br />
                        <img src={cropped_image_library} alt="Cropped Image Library" className="center" />
                        <br />
                    </section>
                </section>

                <section id="exploreDI">
                    <br />
                    <h3>Image Segment</h3>
                    <br />
                    <section id="overViewRIFS">
                        <br />
                        <h4><u>Segmentation</u></h4>
                        <br />
                        <p>
                            <b>Overview</b>
                        </p>
                        <p>
                            The current system's image segmentation uses two main methods for segmenting a cropped image: Watershed Algorithm, Simple Linear Iterative Clustering (SLIC) Algorithm, Quickshift Algorithm and Felzenszwalb Algorithm. In addition to these two methods, there are also multiple forms of pre-processing and post-processing to help produce the best possible segmentation results. Once segmentation is completed, an image preview is presented to allow the user to view the segmentation before deciding to save it. In some cases, multiple previews are generated allowing the user to pick which image they wish to save.
                        </p>
                        <p>
                            <b>How does it work?</b>
                        </p>
                        <p>
                            Discover various segmentation methods by clicking these buttons.
                        </p>

                        <div style={{ display: "flex" }}>
                            <br />
                            <div style={{ display: "block" }}>
                                <button id="quickshift_seg" type="button" className="action-button">
                                    Quickshift Segmentation
                                </button>

                                <div id="quickshifted_seg" style={{ display: "none" }}>
                                    <br />
                                    <br />
                                    <p>
                                        The First method, Quickshift, is an image segmentation technique that efficiently generates superpixels by utilizing the Quickshift algorithm. Quickshift works by estimating the mode-seeking process in the feature space, providing a flexible approach to segmenting images. Key factors in the Quickshift method include:
                                    </p>
                                    <p>
                                        Gauss Sigma: This parameter determines the level of Gaussian blurring applied to the image for smoothing.
                                    </p>
                                    <p>
                                        Kernel Size: The size of the kernel used during the mode-seeking process.
                                    </p>
                                    <p>
                                        Max Distance: The maximum distance allowed for linking pixels in the Quickshift algorithm.
                                    </p>
                                </div>
                            </div>

                            <div style={{ display: "block" }}>
                                <br />
                                <button id="SLIC_seg" className="action-button" style={{ marginLeft: "45px" }} type="button">
                                    SLIC Segmentation
                                </button>

                                <div id="SLICed_seg" style={{ display: "none", marginLeft: "45px" }}>
                                    <br />
                                    <p>
                                        The Second method, SLIC (Simple Linear Iterative Clustering), is a popular image segmentation technique that efficiently generates compact and nearly uniform superpixels. SLIC works by clustering pixels in the combined five-dimensional color and image plane space. This clustering is usually done using the KMeans algorithm. The superpixels generated by SLIC are used to achieve image segmentation. Key factors in the SLIC method include:
                                    </p>
                                    <p>
                                        Gauss Sigma: This parameter determines the level of Gaussian blurring applied to the image for smoothing.
                                    </p>
                                    <p>
                                        Kernel Size: The size of the kernel used for feature extraction during segmentation.
                                    </p>
                                    <p>
                                        Max Distance: The maximum allowed distance for clustering pixels based on similarity and proximity.
                                    </p>
                                </div>
                            </div>

                            <div style={{ display: "block" }}>
                                <br />
                                <button id="water_seg" type="button" style={{ marginLeft: "45px" }} className="action-button">
                                    Watershed Segmentation
                                </button>

                                <div id="watershed_seg" style={{ display: "none" }}>
                                    <br />
                                    <p>
                                        The Third method is the Watershed Algorithm. Before segmentation can begin, we must collect data from the image to be
                                        used for the segmentation. The image is denoised with a Gaussian blur, helping to smooth out the image. The level of blurring
                                        is based on the Gauss Sigma. A gradient filter is then applied to the image after the blurring is completed. The gradient image
                                        is used to generate markers on the image based on a threshold value from feature separation. Once we have the gradient image and
                                        markers generated, we have all the data required to perform the watershed segmentation. The algorithm uses the gradient image and
                                        markers to generate segmentation.
                                    </p>
                                </div>
                            </div>

                            <div style={{ display: "block" }}>
                                <br />
                                <button id="felzenszwalb_seg" type="button" style={{ marginLeft: "45px" }} className="action-button">
                                    Felzenszwalb Segmentation
                                </button>

                                <div id="felzenszwalbed_seg" style={{ display: "none" }}>
                                    <br />
                                    <p>
                                        The Fourth method, Felzenszwalb, is an image segmentation technique that utilizes the Felzenszwalb algorithm to generate superpixels.
                                        The algorithm is based on a hierarchical segmentation strategy that recursively merges image regions based on a similarity measure.
                                        Key factors in the Felzenszwalb method include:
                                    </p>
                                    <p>
                                        Gauss Sigma: This parameter determines the level of Gaussian blurring applied to the image for smoothing.
                                    </p>
                                    <p>Scale: A parameter used to calculate the minimum number of pixels that an object must contain.

                                    </p>
                                    <p>Minimum Size: The minimum size of an image region that is allowed to exist in the final segmentation.

                                    </p>
                                </div>
                            </div>
                        </div>

                        <br />
                        <p>
                            <b>Image Pre-Processing & Post-Processing</b>
                        </p>
                        <p>
                            While the segmentation methods above are great, they are not perfect. In addition, not every image is the same. There are image
                            pre-processing and post-processing methods used to improve the quality of the segmentation. This ensures that every image can
                            be used as effective training data in diverse conditions. As the name suggests Pre-Processing is image processing performed
                            before the segmentation begins for each algorithm. Post-Processing is performed after the segmentation is completed to manipulate
                            the already generated segments before it is presented to the user.
                        </p>

                        <div style={{ display: "flex" }}>
                            <br />
                            <div style={{ display: "block" }}>
                                <br />
                                <button id="PRE_seg" className="action-button" type="button">
                                    Pre-Processing
                                </button>

                                <div id="PREed_seg" style={{ display: "none", marginLeft: "45px" }}>
                                    <br />
                                    <p>
                                        Light Adjustment:- The quality of lighting in an image heavily affects the quality of segmentation. Thus, when this is selected,
                                        3 additional previews are generated with varying lighting adjustments that were made before segmentation. The additional previews
                                        use different algorithms. The algorithms are Histogram Equalization, Adaptive Equalization, and Contrast Limited Adaptive Histogram
                                        Equalization (CLAHE). Each of these methods produce different results that can increase or decrease the quality of segmentation.
                                        In most cases, it is recommended for light adjustment to be used on poorly lit or dark images. However it can be used on brighter
                                        images with varying results.
                                    </p>
                                    <ol>
                                        <li>Histogram Equalization: This method works by taking a Histogram or graph of the entire image’s pixel intensities.
                                            It then levels out the intensities by distributing them evenly across the histogram by utilizing the full range of intensities
                                            and regenerating the image. A disadvantage of this method is that it is indiscriminate. Since it utilizes the full histogram,
                                            it may increase the contrast of background noise while decreasing the useable signal. </li>
                                        <br />
                                        <li>Adaptive Equalization: This method is a modification of the Histogram Equalization. Instead of calculating the whole
                                            image at once it breaks the image into different parts called sub-histograms. This helps emphasize local contrast in parts
                                            of the image rather than the global contrast. The downside is that it can overamplify the contrast.</li>
                                        <br />
                                        <li>CLAHE: A further modification of the Histogram Equalization and Adaptive Equalization. While, the adaptive method tends
                                            to overamplify the contrast in an image causing certain sections to be noisy, this method limits the contrast to prevent
                                            over amplification and generally produces the most “realistic” lighting enhancements</li>
                                        <br />

                                        <div className="image-row">
                                            <br />
                                            <div className="image-column">
                                                <br />
                                                <img style={{ width: "256px", height: "256px" }} src={Originaldms} alt="Image1" />
                                                <div className="image-title">
                                                    Original Image
                                                </div>
                                                <br />
                                            </div>

                                            <div className="image-column">
                                                <br />
                                                <img style={{ width: "256px", height: "256px" }} src={HistEqualDMs} alt="Imag2e" />
                                                <div className="image-title">
                                                    Histogram Equalization
                                                </div>
                                                <br />
                                            </div>
                                        </div>

                                        <div className="image-row">
                                            <br />
                                            <div className="image-column">
                                                <br />
                                                <img style={{ width: "256px", height: "256px" }} src={AdapEqualDms} alt="Image 3" />
                                                <div className="image-title">
                                                    Adaptive Equalization
                                                </div>
                                                <br />
                                            </div>

                                            <div className="image-column">
                                                <br />
                                                <img style={{ width: "256px", height: "256px" }} src={CLAHEdms} alt="Image 4" />
                                                <div className="image-title">
                                                    CLAHE
                                                </div>
                                                <br />
                                            </div>
                                        </div>
                                    </ol>
                                    <br />
                                    <p>
                                        Contrast Stretching:- Though this method works similarly to Histogram Equalization, it is not quite the same. Contrast Stretching takes the highest and lowest pixel intensities and increases the distance between them before leveling out the rest between that range. It produces similar results to Histogram Equalization. However, it is different from histogram equalization as histogram equalization levels out the histogram of an entire image rather than increasing the direct contrast. It can even be stacked with Histogram Equalization to possibly produce better results.
                                    </p>
                                    <br />
                                    <p>
                                        Color Clustering:-  This method works by taking in the dominant colors in an image. It then quantizes the palette(total colors) of the image to a reduced palette only consisting of these dominant colors. This results in a “simplified” image that can improve segmentation due to a smaller number of features to compute during the segmentation process. The number of colors an image is reduced to is based on the number of clusters set by the user. There are two methods used for this: Adaptive and KMeans. It is not recommended to set the clusters to 1 unless you are trying to generate a single segment since it will result in a blank image of 1 color.
                                    </p>
                                    <ol>
                                        <li>Adaptive: Uses the Python Image Library built in method for image color quantization and reduces the palette. A disadvantage is that the colors quantized are not always accurate. However, this usually does not matter. </li>
                                        <li>KMeans: This is the the same algorithm used in SLIC segmentation. It creates cluster points and assigns pixels to the points in multiple iterations. Each iteration is compared with each other to make sure the dominant colors generated are as accurate as possible. </li>
                                    </ol>
                                    <br />
                                    <div className="image-row">
                                        <br />
                                        <div className="image-column">
                                            <br />
                                            <img style={{ width: "256px", height: "256px" }} src={Originaldms} alt="Image1" />
                                            <div className="image-title">
                                                Original Image
                                            </div>
                                        </div>

                                        <div className="image-column">
                                            <br />
                                            <img style={{ width: "256px", height: "256px" }} src={kmean4} alt="Imag2e" />
                                            <div className="image-title">
                                                KMeans 4 Color Clusters
                                            </div>
                                            <br />
                                        </div>
                                    </div>
                                    <div className="image-row">
                                        <br />
                                        <div className="image-column">
                                            <br />
                                            <img style={{ width: "256px", height: "256px" }} src={adap4} alt="Image 3" />
                                            <div className="image-title">
                                                Adaptive 4 Color Clusters
                                            </div>
                                            <br />
                                        </div>

                                        <div className="image-column">
                                            <br />
                                            <img style={{ width: "256px", height: "256px" }} src={kmean1} alt="Image 4" />
                                            <div className="image-title">
                                                KMeans 1 Color Cluster
                                            </div>
                                            <br />
                                        </div>
                                    </div>

                                    <div className="image-row">
                                        <br />
                                        <div className="image-column">
                                            <br />
                                            <img style={{ width: "256px", height: "256px" }} src={kmean2} alt="Image 3" />
                                            <div className="image-title">
                                                KMeans 2 Color Clusters
                                            </div>
                                            <br />
                                        </div>

                                        <div className="image-column">
                                            <br />
                                            <img style={{ width: "256px", height: "256px" }} src={kmean3} alt="Image 4" />
                                            <div className="image-title">
                                                KMeans 3 Color Clusters
                                            </div>
                                            <br />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div style={{ display: "block" }}>
                                <br />
                                <button id="POST_seg" className="action-button" style={{ marginLeft: "45px" }} type="button">
                                    Post-Processing
                                </button>

                                <div id="POSTed_seg" style={{ display: "none", marginLeft: "45px" }}>
                                    <br />
                                    <p>
                                        Region Merging: This method creates a Region Adjacency Graph (RAG) of the segments generated from the segmentation methods. It then compares the generated segment with each other and merges similar
                                        ones based on their average pixel intensities using a threshold set by the user. It helps to reduce over segmentation, especially if a region or feature generated multiple segments that is preferred to be one.
                                        There are 3 different variations for Region Merging: Threshold Cut, Normalized Cut, and Hierarchical. It is highly recommended to use this with SLIC as the algorithm was designed to work hand in hand with SLIC.
                                    </p>
                                    <br />
                                    <p>
                                        Threshold Cut: This is the default region merging method. It compares each segment with its neighboring segments. If neighboring segments fall within the threshold they will be merged into one.
                                        If a segment falls within the threshold for a segment that as already been merged they will be merged all together. For example, if you had a image with 3 segments and segment 1 falls within
                                        the merge threshold for segment 2 but not for segment 3 and segment 3 falls within the threshold for segment 2, they will sill all be merged together. This can be considered a disadvantage in some cases,
                                        but this issue is fixed with the hierarchical method.
                                    </p>
                                    <br />
                                    <p>
                                        Hierarchical: Similar to threshold cut but after each segment merge, it will consider the average of the newly merged segment before merging again rather than comparing each segment by itself.
                                    </p>
                                    <br />
                                    <p>
                                        Normalized Cut: This region merging method is meant to run as a zero parameter mode of region merging. The threshold value normally set by the user is disabled and set automatically in code for the user.
                                        This makes an easier experience for the user but takes away the ability to “fine-tune” the threshold when using region merging.
                                    </p>
                                </div>
                            </div>
                        </div>
                        <br />
                        <p>
                            <b>Segmenting an Image</b>
                        </p>
                        <p>
                            To access the segmentation tool, click on "Segmentation Tool" in the navigation panel.
                        </p>
                        <br />
                        <img src={segmentation_navbar} alt="Edit Profile" className="center" />
                        <br />
                        <p>
                            Upon loading the Image Segmentation Tool, the cropped images will load in a bar at the top of the page. You can navigate to different cropped images by scrolling or clicking the arrows. To select a cropped image
                            for segmentation, click on an image in the bar displaying the cropped images. The segmentation tool will be disabled and display a placeholder image until you select a cropped image. Once you select a cropped image,
                            an enlarged view of it will load in the image box.
                        </p>
                        <br />
                        <p><u>Overview</u></p>
                        <p>1 – Cropped Image Selection </p>
                        <p>2 – Navigation Panel</p>
                        <p>3 – Image Panel</p>
                        <p>4 – Segmentation Settings Panel</p>
                        <p>5 – Image Box</p>
                        <p>6 – Auto Cropping</p>
                        <br />
                        <img src={segmentedit} alt="Edit Profile" className="center" />
                        <br />
                        <p><u>Cropped Image Selection</u></p>
                        <p>
                            The Cropped Image Selection displays images cropped from the tiff images as well as the date they were cropped. The user can use their scroll wheel while hovering their mouse over the selection
                            area to rotate between different cropped images or can click on the arrows on either side of the selection tool to move from right or left. To select a cropped image, simply click on the image you wish to segment.
                        </p>
                        <p>
                            To access the Cropped Image location, click on the navigation icon in the toolbar.
                        </p>
                        <br />
                        <img src={cropimageplacement} alt="Edit Profile" className="center" />
                        <br />
                        <p><u>Image Panel </u></p>
                        <p>
                            Once a cropped image is selected, the Image Panel will populate with any segmentations generated previously using that cropped
                            image. It is sorted by date from newest to oldest and displays the settings used to create that segmentation as well as the date
                            it was created.
                        </p>
                        <p>1 – Segmentation Generated </p>
                        <p>2 – Segmentation Method and Settings </p>
                        <p>3 – Date Segmentation Generated</p>
                        <br />
                        <img src={ImagePanleDisplay} alt="Edit Profile" style={{ height: "300px", width: "150px" }} className="center" />

                        <br />
                        <p><u>Image Box </u></p>
                        <p>
                            Once a cropped image is selected it will appear in the image box along with the name of its parent image from which it was cropped.
                        </p>
                        <img style={{ width: "250px", height: "270px" }} src={canvasimagep} alt="Edit Profile" className="center" />

                        <br />
                        <p><u>Segmentation Settings Panel</u></p>
                        <p>Clicking on the tabs will expand them to show their parameters</p>
                        <p>
                            To select which segmentation algorithm you want, click on the drop down menu next to “Select Segmentation Method”.
                        </p>
                        <br />
                        <img src={Segmentation_dropdown} alt="Edit Profile" className="center" />

                        <br />

                        <p>
                            If a parameter has extra parameters related to it such as the threshold value for region merging, it will reveal itself when that setting is selected.
                        </p>
                        <br />
                        <img style={{ width: "200px", height: "175px" }} src={PP_revealTab} alt="Edit Profile" className="center" />
                        <br />
                        <p>Hovering over any of the settings/parameters will show tool tips related to it.</p>
                        <img style={{ width: "300px", height: "105px" }} src={Seg_hover} alt="Edit Profile" className="center" />
                        
                        <p>Once the desired settings are set, click mark boundaries to generate the segmentation.</p>
                        <img style={{ width: "200px", height: "50px" }} src={MarkBoundariesbt} alt="Edit Profile" className="center" />
                        <br />
                        <p>
                            After you click mark boundaries an Image Preview box will open to allow you to preview the segmentation before saving it.
                            If you do not wish to save the segmentation, click the “X” in the top right corner of the preview box to cancel.
                            Otherwise, click “Save” to save the segmentation to the database.
                        </p>
                        <br />
                        <img src={lightadjustmetnpre} alt="Edit Profile" className="center" />
                        <br />


                    </section>

                    <section id="AutoCrop">
                        <h4><u>Auto Cropping</u></h4>
                        <br />
                        <p>
                            To switch to auto crop, turn on the "Auto Cropping" switch:
                        </p>
                        <br />
                        <img src={AutoCropSwitch} alt="Grid Image" className="center" style={{ height: "35px", width: "150px" }} />

                        <br />
                        <p>
                            After that, the system will present a slider with multiple DMS TIFF images for selection. Once you have chosen a specific DMS TIFF image from the slider, a grid image will appear below, as shown:
                        </p>
                        <br />
                        <img src={AutoGridePage} alt="Grid Image" className="center" />

                        <br />
                        <p>
                            In this grid image, you can conveniently select the region you wish to segment. Simply click and drag your mouse to draw a bounding
                            box around the desired region. The selected region will be displayed on the image canvas, allowing you to proceed with the segmentation process.
                        </p>
                        <br />
                        <p>
                            After selecting the desired region for segmentation, the image canvas will present the chosen area, and you can now move forward with the segmentation process.
                        </p>
                        <br />
                        <img src={GridSelection} alt="Grid Image" className="center" />
                        <br />
                    </section>

                    <section id="classificationschema">
                        <br />
                        <h4><u>Segment Labelling</u></h4>
                        <br />

                        <p>
                            The current system classifies the surface depicted in images into four categories: 1) thick ice (snow-covered or white ice),
                            2) thin ice (gray ice), 3) open water, and 4) shadow (white ice appearing dark due to the presence of shadows).The ClassX
                            system uses the following classification schema to classify uploaded images.
                        </p>
                        <br />

                        <div style={{ display: "block" }}>
                            <img src={labelPage} alt="Classification Schema" className="center" />
                            <br />
                        </div>

                        <div id="classificationTable" >
                            <br />
                            <table className="custom-table">
                                <thead>
                                    <tr>
                                        <th scope="col">Category</th>
                                        <th scope="col">Description</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Ice/Snow</td>
                                        <td>Thick, snow-covered ice which appears white and has a rough surface texture.</td>
                                    </tr>
                                    <tr>
                                        <td>Unknown</td>
                                        <td>Unknown or Unidentifiable regions.</td>
                                    </tr>
                                    <tr>
                                        <td>Thin Ice</td>
                                        <td>Thin, freshly-formed ice which appears gray and has a smooth surface texture.</td>
                                    </tr>
                                    <tr>
                                        <td>Submerged Ice</td>
                                        <td>Thin, freshly-formed ice which appears gray and has a smooth surface texture.</td>
                                    </tr>
                                    <tr>
                                        <td>Melt Pond</td>
                                        <td>Thin, freshly-formed ice which appears gray and has a smooth surface texture.</td>
                                    </tr>
                                    <tr>
                                        <td>Water</td>
                                        <td>Open water appears completely black.</td>
                                    </tr>
                                    <tr>
                                        <td>Shadow</td>
                                        <td>Snow-covered white ice which appears dark due to shadows from overarching ridges or snow dunes.</td>
                                    </tr>
                                </tbody>
                            </table>

                        </div>
                        <div id="canvasIcons">
                            <br />
                            <p><b>Canvas View Options</b></p>
                            <br />
                            <img src={Iconbar} style={{ height: "230px", width: "237px" }} alt="Classification Schema" className="center" />
                            <br />
                            <p>
                                Once you have successfully segmented and labeled your images, you can explore and visualize the results using different view options. The canvas view icons allow you to switch between various representations of the segmented images:
                            </p>
                            <p>
                                <br />
                                <img src={Piecharticon} style={{ height: "30px", width: "37px" }} alt="Pie Chart Icon" className="icon" />
                                <br />
                                Pie Chart View: This view displays the segmented regions as a pie chart, where each segment is represented by a unique color and the corresponding label is shown in the legend.
                            </p>
                            <p>
                                <br />
                                <img src={BargraphIcob} style={{ height: "30px", width: "37px" }} alt="Bar Graph Icon" className="icon" />
                                <br />
                                Bar Graph View: In this view, the segmented regions are represented as a bar graph, with each segment's area proportion displayed on the y-axis and the labels shown on the x-axis.</p>
                            <p>
                                <br />
                                <img src={ImageViewIcon} style={{ height: "30px", width: "37px" }} alt="Crop Icon" className="icon" />
                                <br />
                                Crop View: Clicking this icon will display the original cropped image without any segments or labels, allowing you to view the raw image data.</p>

                            <p>
                                By toggling between these view options, you can gain different insights into your segmented images, making it easier to interpret and analyze the data effectively. These visual representations provide an intuitive way to explore and understand the results of the image segmentation and labelling process.
                            </p>
                            <br />
                        </div>

                        <div id="autoLabelling">
                            <br />
                            <p><b>Auto Labelling</b></p>
                            <p>
                                To auto-label the segments, click on the "Auto Labelling" button:
                            </p>
                            <br />
                            <img src={ButtonAutoLabel} alt="Grid Image" className="center" />

                            <br />
                            <p>
                                After clicking the "Auto Labelling" button, the system will provide you with options for different auto-labelling methods, such as:
                            </p>

                            <p>1. SVM</p>
                            <p>2. Random Forest</p>
                            <p>3. XGBoost</p>
                            <p>4. KNN</p>

                            <p>
                                Choose the most appropriate method based on your specific needs.
                            </p>
                            <p>
                                Additionally, you can fine-tune the auto-labelling process by adjusting the "Probability Threshold" using the slider as shown below:
                            </p>
                            <p>
                                Once you have decided on the method and set the desired labelling threshold, click the "Confirm" button to initiate the auto-labelling process on your segments.
                            </p>
                            <br />
                            <img src={AutoLabelbar} alt="Grid Image" className="center" />
                            <br />

                            <p>
                                The auto-labelling program will efficiently analyze your segments and apply labels based on the chosen method and threshold. This will save you time and effort in manually labeling each segment, enhancing the overall segmentation process.
                            </p>
                            <p>
                                With the Auto Labelling feature, you can quickly and accurately label your segments, making it easier to analyze and categorize the images in your collection effectively.
                            </p>
                            <p><b>Save Labeled Files</b></p>
                            <p>To save labeled files, follow these steps:</p>
                            <p>
                                1. Choose the file format you want to save the labeled data as, either HDF5 or COCO, from the available options.
                            </p>
                            <br />
                            <img src={Savefile_dropdown} alt="Grid Image" className="center" />
                            <br />
                            <p>
                                2. After labeling the segments in the image, click on the "Save" button
                                <img src={Savebuttonlabel} style={{ width: "40px", height: "30px" }} alt="Grid Image" />.
                            </p>
                            <p>3. A popup window titled "Save Labeling" will appear.</p>
                            <br />
                            <img src={savefilemodal} style={{ width: "200px", height: "110px" }} alt="Grid Image" className="center" />
                            <br />
                            <p>
                                4. In the popup window, enter the desired name for the labeled file in the input field provided.
                            </p>
                            <p>
                                5. If you wish to save the labeled data as a new file, Choose "Create New" from the drop down. The labeled data will be saved as a new file with the specified name and file format.
                            </p>
                            <br />
                            <img src={savefiledropdown} style={{ width: "200px", height: "40px" }} alt="Grid Image" className="center" />
                            <br />
                            <p>
                                6. If you want to append the labeled image to an already existing file, Choose the "Append to Existing File" from the drop down. You will be prompted to choose the file to which you want to append the labeled data.
                            </p>
                            <p>
                                7. Once you have made your choice and provided the necessary information, click on the "Save" button to save the labeled file. You will receive a confirmation on saving
                            </p>
                            <p>
                                This functionality allows you to efficiently store and manage your labeled data, making it easy to access and share with other ClassX users or external collaborators.
                            </p>
                        </div>
                        <br />
                    </section>
                </section>

                <section id="imageMan">
                    <br />
                    <h3>View & Share</h3>
                    <br />
                    <section id="dataPrep">
                        <br />
                        <h4><u>Viewing Training Datasets</u></h4>
                        <br />
                        <p>
                            To view labeled datasets, click on the "Training Datasets" button in the navigation bar. This will take you to
                            your training datasets library, where you can access your labeled files and datasets. <br />
                            <img src={view_and_share_button} style={{ width: "100px", height: "30px" }} alt="Grid Image" className="center" />
                            <br />
                        </p>
                        <p>
                            On the training datasets page, you will see a list of files and datasets available for viewing.
                            <br />
                            <br />
                            <img src={viewFiles} alt="Grid Image" className="center" />
                            <br />To access a
                            specific file, click on the "View" button
                            <br />
                            <img src={viewbutton} style={{ width: "40px", height: "30px" }} alt="Grid Image" />
                            <br />
                            next to that file's name. This will take you to a page displaying the cropped images from that file.
                        </p>
                        <br />
                        <img src={view_labelcrop} alt="Grid Image" className="center" />
                        <br />
                        <p>
                            On the cropped images page, you can browse through the available labeled cropped images. To view the details
                            of a labeled cropped image, click on the image. This will open a modal displaying the labeled cropped image.
                        </p>
                        <p>
                            Inside the modal, you can click on the image to access the pie chart that shows the details of the labeling
                            for that cropped image. The pie chart will appear on the top right side of the modal, providing a visual
                            representation of the labeling information.
                        </p>
                        <p>
                            Additionally, you can click on the "Show Crop Location" button to view the region from which the cropped
                            image has been taken. This will provide you with an overview of the image's location within the larger
                            dataset.
                            <br />
                            <br />
                            <img src={imagepreviewvie_and_share} alt="Grid Image" className="center" />
                        </p>
                        <br />
                        {/* Leave space for images and screenshots */}
                    </section>

                    <section id="deleteSUI">
                        <br />
                        <h4><u>Sharing Files</u></h4>
                        <br />
                        <p>To share files with other ClassX users, follow these steps:</p>
                        <p>1. On the View and Share page, locate the file you want to share in the table.</p>
                        <p>2. Click on the "Share" button <br /> <img src={shareIcon} style={{ width: "40px", height: "25px" }} alt="Grid Image" /> <br /> at the top of the table.</p>
                        <p>3. A popup window titled "Share" will appear.</p>
                        <p>4. In the dropdown menu, you will find a list of ClassX users.</p>
                        <p>5. Click on the checkbox next to the username of the person you want to share the file with.</p>
                        <p>6. Alternatively, select the checkbox next to "All" to share the file with all ClassX users.</p>
                        <p>7. Once you have selected the user(s) to share with, click on the "Share" button at the bottom right corner of the popup window.</p>
                        <br />
                        <img src={shareodaloptions} style={{ height: "150px", width: "260px" }} alt="Grid Image" className="center" />
                        <br />
                        <p>
                            After clicking "Share," the system will send the shared file to the selected user(s). You will receive a confirmation message once the sharing process is completed. The user(s) you shared the file with will also receive a notification about the shared file.
                        </p>
                        <br />
                        <img src={Share_confo} style={{ height: "75px", width: "250px" }} alt="Grid Image" className="center" />
                        <br />
                        <p>This functionality allows you to securely share images and files with other ClassX users, enabling seamless collaboration and information exchange within the ClassX community.</p>
                        <br />
                        {/* Leave space for screenshots or other visuals if needed */}
                    </section>
                </section>
            </Document >
            <Anchor
                affix={false}
                onClick={handleClick}
                style={{ position: "fixed", right: 30 }}
                items={[
                    {
                        key: '1',
                        href: '#introDiv',
                        title: 'Introduction',
                    },
                    {
                        key: '2',
                        href: '#archiDiv',
                        title: 'System Architecture',
                        children: [
                            {
                                key: '3',
                                href: '#userRegAndVer',
                                title: 'User Registration and Verification',
                            },
                            {
                                key: '4',
                                href: '#profileMan',
                                title: 'Image Exploration',
                                children: [
                                    {
                                        key: '5',
                                        href: '#vAndEprofile',
                                        title: 'Image Search & Filter',
                                    },
                                    {
                                        key: '6',
                                        href: '#AliasImage',
                                        title: 'Image Alias',
                                    },
                                ]
                            },
                            {
                                key: '7',
                                href: '#ImageCrop',
                                title: 'Image Crop',
                                children: [
                                    {
                                        key: '8',
                                        href: '#imagesearch',
                                        title: 'Multi - image upload',
                                    },
                                    {
                                        key: '9',
                                        href: '#sendEmail',
                                        title: 'Image Cropping',
                                    },
                                ]
                            },
                            {
                                key: '10',
                                href: '#imageMan',
                                title: 'View & Share',
                                children: [
                                    {
                                        key: '11',
                                        href: '#dataPrep',
                                        title: 'Viewing training Datasets',
                                    },
                                    {
                                        key: '12',
                                        href: '#deleteSUI',
                                        title: 'Sharing file(s)',
                                    },
                                ]
                            },
                        ],
                    },
                ]}
            />
        </div>
    )
};

const Document = styled.div`
    padding: 50px 300px 100px 100px;
    .center{
        width: 700px;
    }
`
export default Help;
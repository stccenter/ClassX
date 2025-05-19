# Python Standard Library Imports
import os
from ctypes import c_int, c_uint32

# Python Third Party Imports
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier

# Local Library Imports
from .analysis import attr_calc

__all__ = ['classify_image']

def classify_image(input_image, segment_image, training_dataset, metadata, prob_threshold, model, saved_model_file_path, needs_retrain):
    """
    Run a random forest classification.
    Input:
        input_image: preprocessed image data (preprocess.py)
        watershed_image: Image objects created with the segmentation
            algorithm. (segment.py)
        training_dataset: Tuple of training data in the form:
            (label_vector, attribute_matrix)
        meta_data: [im_type, im_date]
        model: [
            0: svm
            1: random forest
            2: xgboost
            3: knn
        ]
        saved_model_file_path: path
        needs_retrain: needs to retrain or read model
    Returns:
        Raster of classified data.
    """

    #### Prepare Data and Variables
    image_type = metadata[0]
    image_domain = metadata[1]

    ## Parse training_dataset input
    label_vector = training_dataset[0]
    training_feature_matrix = training_dataset[1]

    ## get training folder
    if model == 0:
        #If it needs retrain removing the old model
        if needs_retrain == True:
            #Removing old model
            if os.path.exists(saved_model_file_path):
                os.remove(saved_model_file_path)
            #Creating the model classifer
            classifer = svm.SVC(probability=True, C = 100, kernel='rbf')

            #Fitting the training data to the model
            classifer.fit(training_feature_matrix, label_vector)

            #Dumping the data
            joblib.dump(classifer, saved_model_file_path)
        else:
            #Loading prexisting model
            classifer = joblib.load(saved_model_file_path)
    elif model == 1:
        #If it needs retrain removing the old model
        if needs_retrain == True:
            #Removing old model
            if os.path.exists(saved_model_file_path):
                os.remove(saved_model_file_path)
            #Creating the model classifer
            classifer = RandomForestClassifier(min_samples_split = 2, n_estimators=100)

            #Fitting the training data to the model
            classifer.fit(training_feature_matrix, label_vector)

            #Dumping the data
            joblib.dump(classifer, saved_model_file_path)
        else:
            #Loading prexisting model
            classifer = joblib.load(saved_model_file_path)
    elif model == 2:
        #### xgboosts needs retrain to build mapping everytime
        classifer = xgb.XGBClassifier(max_depth=5,learning_rate=0.1,n_estimators=1000,subsample=0.8,colsample_bytree=0.8,reg_alpha=0.1,reg_lambda=0.1)

        # xgboost requires y to be [0,1,2,3....] so we have to map our label
        unique_labels = list(set(label_vector))

        # mapping maps 0,1,2 to unique values of label_vector
        mapping = {}

        #rev mapping does the opposite
        reverse_mapping = {}
        mapped_list = []

        #TODO Test what happens if this is not done
        index = 0
        for value in unique_labels:
            #Setting the index number to the label id
            mapping[index] = value

            #Opposite mapping
            reverse_mapping[value] = index
            mapped_list.append(index)
            index += 1
        for index in range(0,len(label_vector)):
            label_vector[index] = reverse_mapping[label_vector[index]]

        #Fitting the training data to the model
        classifer.fit(training_feature_matrix, label_vector)

        #Dumping the data
        joblib.dump(classifer, saved_model_file_path)
    elif model == 3:
        #If it needs retrain removing the old model
        if needs_retrain == True:
            #Removing old model
            if os.path.exists(saved_model_file_path):
                os.remove(saved_model_file_path)

            #Creating the model classifer
            classifer = KNeighborsClassifier(n_neighbors=3)

            #Fitting the training data to the model
            classifer.fit(training_feature_matrix, label_vector)

            #Dumping the data
            joblib.dump(classifer, saved_model_file_path)
        else:
            #Loading prexisting model
            classifer = joblib.load(saved_model_file_path)
    classified_block = classify_block(input_image, segment_image, image_type, image_domain, classifer, 0, 0, prob_threshold)
    # need to fix the mapping for xgboost 
    if model == 2:
        for key, value in classified_block.items():
            if value != -1:
                classified_block[key] = mapping[value]
    return classified_block

def classify_block(image_block, segment_image, image_type, image_date, classifer, wb_ref, bp_ref, prob_threshold):

    # Cast data as C int.
    segment_image = segment_image.astype(c_uint32, copy=False)

    ## If the block contains no data, set the classification values to 0
    if np.amax(image_block) < 2:
        classified_block = np.zeros(np.shape(image_block)[1:3])
        return classified_block
    ## We need the object labels to start at 0. This shifts the entire 
    #   label image down so that the first label is 0, if it isn't already. 
    if np.amin(segment_image) > 0:
        segment_image -= np.amin(segment_image)
    ## Calculate the features of each segment within the block. This 
    #   calculation is unique for each image type. 
    if image_type == 'wv02_ms':
        input_feature_matrix = attr_calc.analyze_ms_image(image_block, segment_image,
                                                          wb_ref, bp_ref)
    elif image_type == 'srgb':
        input_feature_matrix = attr_calc.analyze_srgb_image(image_block,segment_image)
    elif image_type == 'pan':
        input_feature_matrix = attr_calc.analyze_pan_image(
                                image_block, segment_image, image_date)

    input_feature_matrix = np.array(input_feature_matrix)
    # Predict the classification of each segment
    segment_predictions = classifer.predict(input_feature_matrix)
    segment_prob = classifer.predict_proba(input_feature_matrix)
    class_labels = classifer.classes_
    segment_predictions = np.ndarray.astype(segment_predictions, dtype=c_int, copy=False)
    # Create the classified image by replacing watershed id's with
    #   classification values.
    # If there is more than one band, we have to select one (using 2 for 
    #   no particular reason).
    label_dict = {}
    # each row in ws_prob represents a probability mapping 
    for i in range(0,segment_prob.shape[0]):
        cur_max = 0
        max_label = -1
        for j, label in enumerate(class_labels):
            if segment_prob[i][j] > cur_max:
                cur_max = segment_prob[i][j]
                max_label = label
        # if the current max is >= threshold, label it
        if cur_max >= prob_threshold:
            label_dict[i+1] = max_label
        else:
            label_dict[i+1] = -1
    
    return label_dict
import pandas as pd
import numpy as np
import SimpleITK as sitk
from skimage.util import img_as_ubyte
from skimage.morphology import ball
from skimage.filters import rank
from skimage.morphology import disk
import tensorflow as tf
from skimage.color import gray2rgb



from pathlib import Path
from scipy import ndimage
from skimage import exposure
from sklearn.preprocessing import MinMaxScaler

import argparse
import cv2
import os
from numpy import moveaxis

 ## Extracting patches of size : T2-64*64*3, Rest-16*16*3
 #used contrast stretching instead of histogram equalization     

def generate_patches(row, patch_sizes):
 
    reported_pos = row.ijk
      
    path_to_file = row.path_nrrd



    if 't2' in row.DCMSerDescr:        
        patch_size = patch_sizes.get('t2')
    elif 'adc' in row.DCMSerDescr:
        patch_size = patch_sizes.get('adc')
    elif 'bval' in row.DCMSerDescr:
        patch_size = patch_sizes.get('bval')
    else:
        patch_size = patch_sizes.get('ktrans')
    


    def load_image(path_to_file):
        sitk_image = sitk.ReadImage(str(path_to_file))
        #image_array = sitk.GetArrayViewFromImage(sitk_image)
        image_array = sitk.GetArrayFromImage(sitk_image)
        # size_nrrd = sitk_image.GetSize()
        # spacing_nrrd = sitk_image.GetSpacing()
        # print("image size",size_nrrd)
        # print("spacing",spacing_nrrd)
        
        return sitk_image, image_array

    def calculate_location_of_finding(sitk_image, reported_pos):
        location_of_finding = reported_pos
        #print(location_of_finding)
        return location_of_finding

    def equalize_image(image_array):
        
        #equalized_image_array = exposure.equalize_hist(image_array,mask=None)
              
        equalized_image_array = image_array
        return equalized_image_array

    def extract_patch(image_array, location_of_finding, patch_size):
        x = location_of_finding[0]
        y = location_of_finding[1]
        z = location_of_finding[2]

        x_start = x - (patch_size // 2)
        x_end = x + (patch_size // 2)
        y_start = y - (patch_size // 2)
        y_end = y + (patch_size // 2)
        z_start = z - (1) ## extracting 3 slices-so it is a 3d patch
        z_end = z + (2)

        try:
            extracted_patch = image_array[z_start:z_end, y_start:y_end, x_start:x_end]
        except IndexError:
            extracted_patch = image_array[-1, y_start:y_end, x_start:x_end]
            problem_cases.append(row.ProxID)
            problem_cases.append(row.DCMSerDescr)
            print('Problem with image:', row.ProxID, path_to_file)
            pass

              

        return extracted_patch

        
    def rescale_intensities_of_patch(patch):
                
        p2, p98 = np.percentile(patch, (2, 98))
        rescaled_patch = exposure.rescale_intensity(patch, in_range=(p2, p98))
        return rescaled_patch

    sitk_image, image_array = load_image(path_to_file)
    location_of_finding = calculate_location_of_finding(sitk_image,reported_pos)
    # print(location_of_finding)
    
    raw_image_array = image_array.copy()
    equalized_image_array = equalize_image(image_array)
    #equalized_image_array = image_array
    #print(equalized_image_array.shape)
    
    patch = extract_patch(raw_image_array, location_of_finding, patch_size)
    eq_patch = extract_patch(equalized_image_array, location_of_finding, patch_size)
  

    patch_01 = rescale_intensities_of_patch(patch)
    eq_patch_01 = rescale_intensities_of_patch(eq_patch)
    

    eq_patch_01 = moveaxis(eq_patch_01, 0, 2)

    
    #print("extraxted patch shape", eq_patch_01.shape)
    eq_patch_01 = cv2.resize(eq_patch_01, (224, 224),interpolation = cv2.INTER_AREA) #changing size for pretrained model
    
    eq_patch_01 = np.array(eq_patch_01, dtype=np.float, copy = True)
    
   
    print("extracted patch shape", eq_patch_01.shape)

    imgy = sitk.GetImageFromArray(eq_patch_01)
    #print ("sitk_patch =", imgy.GetSize())
    print("spacing_patch = ",imgy.GetSpacing())
    patch_values = pd.Series({'patch':patch_01, 'eq_patch':eq_patch_01})

    return patch_values

    

def persist_data(is_training_data, dataframe):
    if is_training_data:
        dataframe.to_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/Patch_ijk_Training.csv')
        dataframe.to_pickle('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/Patch_ijk_Training.pkl')

def add_patch_columns_to_df(dataframe, patch_sizes):
    new_data = dataframe.apply(generate_patches, patch_sizes = patch_sizes, axis = 1)
    merged_frame = pd.concat([dataframe, new_data], axis=1)
    return merged_frame

def main():
   
    is_training_data = True

    patch_sizes = {
        't2': 64,
        'adc': 16,
        'bval': 16,
        'ktrans':16
    }
    
    if is_training_data:
        
        dataset = pd.read_pickle('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/SampleTraining1.pkl')
        #dataset = pd.read_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/SampleTraining1.csv')
        complete_dataset = add_patch_columns_to_df(dataset, patch_sizes)

        persist_data(is_training_data, complete_dataset)

main()

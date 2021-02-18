"""
Description: This script generates the numpy arrays that will be used in 
deep learning models.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_image_sequence(is_training_data, data):
    t2tra_sequence = data[data['sequence_type'] == 't2tra']
    t2sag_sequence = data[data['sequence_type'] == 't2sag']
    adc_sequence = data[data['sequence_type'] == 'adc']
    bval_sequence = data[data['sequence_type'] == 'bval']
    ktrans_sequence = data[data['sequence_type'] == 'ktrans']
    

    def balance_classes(sequence):
        
        patch_sequence = []
        significance_sequence = []
        # including rotations of all grade cancers
        for row_id, row in sequence.iterrows():
            if row.ggg == row.ggg :


                patch_sequence.append(row.eq_patch)
                significance_sequence.append(row.ggg)
                

            else:
                patch_sequence.append(row.eq_patch)
                significance_sequence.append(row.ggg)

        print((np.array(patch_sequence).shape), (np.array(significance_sequence).shape))
        return (np.array(patch_sequence), np.array(significance_sequence))

        


    
    def zero_mean_unit_variance(image_array):

        # https://stackoverflow.com/questions/41652330/centering-of-array-of-images-in-python
        # https://stackoverflow.com/questions/36394340/centering-a-numpy-array-of-images
        #print(image_array)
       
        image_array_float = np.array(image_array, dtype=np.float, copy = True)
        mean = np.mean(image_array_float, axis=(0))
        std = np.std(image_array_float, axis=(0))
        standardized_images = (image_array_float - mean) / std


      
        return standardized_images

    
    t2tra_images, t2tra_findings = balance_classes(t2tra_sequence)
    t2sag_images, t2sag_findings = balance_classes(t2sag_sequence)
    adc_images, adc_findings = balance_classes(adc_sequence)
    bval_images, bval_findings = balance_classes(bval_sequence)
    ktrans_images, ktrans_findings = balance_classes(ktrans_sequence)
        
    print("Eg: T2tra-images,findings- Array Shape :", t2tra_images.shape, t2tra_findings.shape)
    
    t2tra_norm = zero_mean_unit_variance(t2tra_images)
    t2sag_norm = zero_mean_unit_variance(t2sag_images)
    adc_norm = zero_mean_unit_variance(adc_images)
    bval_norm = zero_mean_unit_variance(bval_images)
    ktrans_norm = zero_mean_unit_variance(ktrans_images)

    return {'t2tra':(t2tra_norm, t2tra_findings),
            't2sag':(t2sag_norm, t2sag_findings), 
            'adc':(adc_norm, adc_findings),
            'bval':(bval_norm, bval_findings),
            'ktrans':(ktrans_norm, ktrans_findings)} 

def persist_numpy_to_disk(is_training_data, data):
    t2tra_images = data.get('t2tra')[0]
    t2tra_labels = data.get('t2tra')[1]

    t2sag_images = data.get('t2sag')[0]
    t2sag_labels = data.get('t2sag')[1]

    adc_images = data.get('adc')[0]
    adc_labels = data.get('adc')[1]

    bval_images = data.get('bval')[0]
    bval_labels = data.get('bval')[1]

    ktrans_images = data.get('ktrans')[0]
    ktrans_labels = data.get('ktrans')[1]

    if is_training_data:
        root_path = 'D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/numpy/ijk/'
        
        np.save(Path(root_path + '/t2sag/X_train_ijk.npy'), t2sag_images)
        np.save(Path(root_path + '/t2sag/Y_train_ijk.npy'), t2sag_labels)

        np.save(Path(root_path + '/t2tra/X_train_ijk.npy'), t2tra_images)
        np.save(Path(root_path + '/t2tra/Y_train_ijk.npy'), t2tra_labels)

        np.save(Path(root_path + '/adc/X_train_ijk.npy'), adc_images)
        np.save(Path(root_path + '/adc/Y_train_ijk.npy'), adc_labels)

        np.save(Path(root_path + '/bval/X_train_ijk.npy'), bval_images)
        np.save(Path(root_path + '/bval/Y_train_ijk.npy'), bval_labels)

        np.save(Path(root_path + '/ktrans/X_train_ijk.npy'), ktrans_images)
        np.save(Path(root_path + '/ktrans/Y_train_ijk.npy'), ktrans_labels)
    else:
        root_path = 'D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Test/numpy/ijk/'
        
        np.save(Path(root_path + '/t2sag/X_test_ijk.npy'), t2sag_images)
        np.save(Path(root_path + '/t2sag/Y_test_ijk.npy'), t2sag_labels)

        np.save(Path(root_path + '/t2tra/X_train_ijk.npy'), t2tra_images)
        np.save(Path(root_path + '/t2tra/Y_train_ijk.npy'), t2tra_labels)

        np.save(Path(root_path + '/adc/X_test_ijk.npy'), adc_images)
        np.save(Path(root_path + '/adc/Y_test_ijk.npy'), adc_labels)

        np.save(Path(root_path + '/bval/X_test_ijk.npy'), bval_images)
        np.save(Path(root_path + '/bval/Y_test_ijk.npy'), bval_labels)

        np.save(Path(root_path + '/ktrans/X_test_ijk.npy'), ktrans_images)
        np.save(Path(root_path + '/ktrans/Y_test_ijk.npy'), ktrans_labels)

def main():
    
    is_training_data = True

    if is_training_data:
        data = pd.read_pickle('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/Patch_ijk_Training.pkl')
    else:
        data = pd.read_pickle('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Test/dataframes/Patch_ijk_Testing.pkl')
    
    numpy_data = generate_image_sequence(is_training_data, data)
    persist_numpy_to_disk(is_training_data, numpy_data)

main()
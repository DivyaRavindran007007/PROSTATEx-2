      

import os
import pandas as pd
import pickle
from pathlib import Path
from pandas import DataFrame


def generate_DCMSerDescr_from_filename(item):
        # remove extension from path
        full_name = item
        split = full_name.split('.')
        name_without_extension = split[0]
        first_underscore = name_without_extension.find('_') + 1
        dscr = name_without_extension[first_underscore:]
        # value = dscr.split('_')[:-1]
        s2 = '_'.join(word for word in dscr.split('_') if not word.isdigit())
        s3 = s2.lower()
        
        prox = name_without_extension.split('_')
        ID = prox[0]
        return ID,s3

def convert_to_tuple(dataframe, column):
        """
        This function converts row values (represented as string of floats
        delimited by spaces) to a tuple of floats. It accepts the original data
        frame and a string for the specified column that needs to be converted.
        """  
        
        pd_series_containing_lists_of_strings = dataframe[column].str.split() 
        list_for_new_series = []
        for list_of_strings in pd_series_containing_lists_of_strings:
            container_list = []
            for item in list_of_strings:
                if column == 'pos':
                    container_list.append(float(item))
                else:
                    container_list.append(int(item))
            list_for_new_series.append(tuple(container_list))
        return pd.Series(list_for_new_series) 
        


def main():

    prostateX_images = pd.read_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/Final-with-Ktrans.csv')
    prostateX_images.loc[:,'DCMSerDescr'] = prostateX_images.loc[:,'DCMSerDescr'].apply(lambda x: x.lower())

    path_to_nifti = Path('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/Training/intermediate/nrrd-train/')
    l1 = []
    l2 = []
    patient_nrrds = os.listdir(path_to_nifti)
    for i in patient_nrrds:
        Path_to_nrrd = path_to_nifti/i

        ProxID,constructed_DCMSerDescr = generate_DCMSerDescr_from_filename(i)
        if 't2_tse_tra' in constructed_DCMSerDescr:
            sequence_type = 't2tra'
        elif 't2_tse_sag' in constructed_DCMSerDescr:
            sequence_type = 't2sag'
        elif 'adc' in constructed_DCMSerDescr:
            sequence_type = 'adc'
        elif 'bval' in constructed_DCMSerDescr:
            sequence_type = 'bval'
        else:
            sequence_type = 'ktrans'
        key = ProxID    
        value = [constructed_DCMSerDescr, Path_to_nrrd, sequence_type]
        l1.append(key)
        l2.append(value)


    df1 = DataFrame (l2,columns=['DCMSerDescr','path_nrrd', 'sequence_type'])
    df2 = DataFrame (l1,columns=['ProxID'])
    cases_meta_data_df = pd.merge(df1, df2, left_index=True, right_index=True)
    # cases_meta_data_df.loc[:,'DCMSerDescr'] = cases_meta_data_df.loc[:,'DCMSerDescr'].apply(lambda x: x.lower())
    #cases_meta_data_df.to_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/Sampletrain.csv')
    first_merge = pd.merge( prostateX_images,cases_meta_data_df, how = 'inner', on = ['ProxID', 'DCMSerDescr'])


    # first_merge.to_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/Test.csv')
    # print(type(first_merge))
    # print(type(first_merge['pos']))
    # print(first_merge.dtypes)
    # first_merge= first_merge.stack()

    # first_merge = first_merge.ix[:,2] 


    # Converting pos and ijk into tuple
    Trainingdata1 = first_merge.assign(pos_tuple = convert_to_tuple(first_merge, 'pos'))

    Trainingdata = Trainingdata1.assign(ijk_tuple = convert_to_tuple(Trainingdata1, 'ijk'))
    # print(Trainingdata.dtypes)
    
    # Drop old columns, rename new ones, and reorder...
    Trainingdata = Trainingdata.drop(columns = ['pos','ijk'])
    Trainingdata = Trainingdata.rename(columns = {'pos_tuple':'pos', 'ijk_tuple':'ijk'})
    Trainingdata.to_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/SampleTraining1.csv')
    Trainingdata.to_pickle('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/SampleTraining1.pkl')

main()





#prostateX_images = prostateX_images.rename(columns = {'pos_tuple':'pos', 'ijk_tuple':'ijk'})










# prostateX_images.to_csv('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/training_meta_data1.csv')
# prostateX_images.to_pickle('D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/GithubCodeNrrd/Train/dataframes/training_meta_data.pkl')

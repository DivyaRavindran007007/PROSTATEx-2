import os

''' NOTE: This file will run in Slicer python interactor.
NOTE: Make sure that the following directories are consistent with settings
file.
'''

dicom_root = "D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/Test/PROSTATEx"
#dicom_root = "/project2/rcc/tszasz/MRIRC/Prostate_DeepLearning_Projects/ProstateX/Data_Prep/raw/DOI"
#dicom_root = "/project2/rcc/tszasz/MRIRC/Prostate_DeepLearning_Projects/ProstateX/Data_Prep/TEST/raw/DOI"
ktrans_root = "D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/Test/KtransTest/"
#ktrans_root = "/project2/rcc/tszasz/MRIRC/Prostate_DeepLearning_Projects/ProstateX/Data_Prep/raw/ProstateXKtrains-train-fixed/"
#ktrans_root = "/project2/rcc/tszasz/MRIRC/Prostate_DeepLearning_Projects/ProstateX/Data_Prep/TEST/raw/ProstateXKtrans-test-fixedv2/"
intermediate_folder = "D:/MSCA/CAPSTONE/Prostate2Challenge-Team2/Test/intermediate/"
#intermediate_folder = "/project2/rcc/tszasz/MRIRC/Prostate_DeepLearning_Projects/ProstateX/Data_Prep/intermediate/"
outputdirectory = os.path.join(intermediate_folder, 'nrrd-test')
#outputdirectory = os.path.join(intermediate_folder, 'nrrd-test')

excluded_patients = []
# excluded_patients = ["ProstateX-0191","ProstateX-0190","ProstateX-0025","ProstateX-0031"]
patient_folders = [patient_folder for patient_folder in sorted(os.listdir(dicom_root))
                   if patient_folder not in excluded_patients]

if not os.path.exists(outputdirectory):
    os.makedirs(outputdirectory)

start_patient = 0
for patient_folder in patient_folders:
    print patient_folder 
    patient_number = int(patient_folder.split('-')[1])
    if patient_number > start_patient:
        patient_folder_path = os.path.join(dicom_root, patient_folder)
        study_folders = sorted(os.listdir(patient_folder_path))
        if len(study_folders) == 1:
            study_folder = study_folders[0]
            study_folder_path = os.path.join(patient_folder_path, study_folder)
            series_folders = sorted(os.listdir(study_folder_path))
            print patient_folder, len(series_folders)
        elif len(study_folders) > 1:
            print "patient has more than one studies: {}".format(patient_folder)
            print "It was not added to the studies collection."
        else:
            print "no study foler for patient:{}".format(patient_folder)
        for series_folder in series_folders:
            series_folder_path = os.path.join(study_folder_path, series_folder)
            file_names = [os.path.join(series_folder_path, file_name) for file_name in os.listdir(series_folder_path)]
            plugin = slicer.modules.dicomPlugins['DICOMScalarVolumePlugin']()
            if plugin:
                loadables = plugin.examine([file_names])
            if len(loadables) == 0:
                print('plugin failed to interpret this series')
            else:
                series_description = slicer.dicomDatabase.fileValue(file_names[0], "0008,103E")
                series_number = slicer.dicomDatabase.fileValue(file_names[0], "0020,0011")
                # print series_description
                required_serires_descriptions = ["t2_tse_tra", "t2_tse_sag", "t2_tse_cor", "ADC", "BVAL"]
                #
                # Load the dicom data
                #
                if any(description in series_description for description in required_serires_descriptions):
                    print 'loading:', series_description
                    volume = plugin.load(loadables[0])
                    volume_name = series_description + '_' + series_number
                    volume.SetName(volume_name)
                    ####
                    output_file_name = patient_folder + '_' + volume_name + '.nrrd'
                    slicer.util.saveNode(volume, os.path.join(outputdirectory, output_file_name))
                    slicer.mrmlScene.RemoveNode(volume)
                    slicer.app.processEvents()
        ktrans_path = ktrans_root + patient_folder + '/' + patient_folder + '-Ktrans.mhd'
        loadVolume(ktrans_path)
        node = getNode(patient_folder + '-Ktrans')
        output_file_name = patient_folder + '_Ktrans' + '.nrrd'
        slicer.util.saveNode(node, os.path.join(outputdirectory, output_file_name))
        slicer.mrmlScene.RemoveNode(node)
        slicer.app.processEvents()

# PROSTATEx-2
SPIE-AAPM-NCI PROSTATEx Challenges-The PROSTATEx Challenge (" SPIE-AAPM-NCI Prostate MR Classification Challenge”) focused on  
quantitative image analysis methods for the diagnostic classification of clinically significant prostate cancers and was held 
in conjunction with the 2017 SPIE Medical Imaging Symposium.  PROSTATEx ran from November 21, 2016 to January 15, 2017, though
a "live" version has also been established at https://prostatex.grand-challenge.org  which serves as an ongoing way for
researchers to benchmark their performance for this task.  The PROSTATEx-2 Challenge (" SPIE-AAPM-NCI  Prostate MR Gleason Grade 
Group Challenge" ) was focused on  the development of quantitative multi-parametric MRI biomarkers for the determination of Gleason
Grade Group in prostate cancer. 

Steps:

1) Convert DICOM images to Nrrd/Nifti format using the Slicer Application
2) Data Exploration & Visualization
3) Preprocessing the data and converting to numpy arrays
4) Model & Results


Note: Eventhough T2 tra, T2 sag, ADC, Bval and ktrans images were used till Step 2, only T2tra, ADC and Bval were used in the model(Reference:2)

References : 

1)Diagnosis of Prostate Cancer by Use of MRI-Derived Quantitative Risk Maps: A Feasibility Study
Aritrick Chatterjee1, Dianning He1,2Xiaobing Fan1 Tatjana Antic3 Yulei Jiang1 Scott Eggener4 Gregory S. Karczmar1 Aytekin Oto1
********************************************************************************************************************************
2)Automated grading of prostate cancer using convolutional neural networkand ordinal class classifier
Bejoy Abraham, Madhu S. Nair
********************************************************************************************************************************
3)MED3D: TRANSFER LEARNING FOR 3D MEDICAL IMAGE ANALYSIS
Sihong Chen∗1, Kai Ma1and Yefeng Zheng1,1Tencent YouTu X-Lab, Shenzhen
********************************************************************************************************************************
4)Single-Label Multi-Class Image Classification by Deep Logistic Regression
Qi Dong,1 Xiatian Zhu,2 Shaogang Gong1
********************************************************************************************************************************
5)Future Perspectives in Multiparametric Prostate MR Imaging
Aritrick Chatterjee, PhD, Aytekin Oto, MD, MBA
********************************************************************************************************************************
6)https://github.com/alexhamiltonRN/ProstateX



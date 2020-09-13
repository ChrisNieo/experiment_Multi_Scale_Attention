import os
import SimpleITK as sitk
from skimage.io import imread, imsave
import numpy as np
import random
import shutil
PATH = "../../DataSet"
MODEL = "Chaos_Challenge"
SOURCE = "MR"
OUT_PUT_DIR = os.path.join(PATH,MODEL)
DATA_ROOT = os.path.join(PATH,MODEL,SOURCE)
flair_name = "_flair.nii.gz"
t1_name = "_t1.nii.gz"
t1ce_name = "_t1ce.nii.gz"
t2_name = "_t2.nii.gz"
mask_name = "_seg.nii.gz"

def get_T1_filename(patient_path):
    gt = []
    img = []
    t1_data_dir = os.path.join(patient_path,"T1DUAL")

    ground_dir = os.path.join(t1_data_dir, "Ground")
    ground_names = os.listdir(ground_dir)
    for i in range(len(ground_names)):
        gt.append(os.path.join(ground_dir,ground_names[i]))

    img_dir = os.path.join(t1_data_dir, "DICOM_anon","InPhase")
    img_names = os.listdir(img_dir)
    for i in range(len(img_names)):
        img.append(os.path.join(img_dir,img_names[i]))
    return gt,img

def get_data_object(root = DATA_ROOT):
    for root,dirs,files in os.walk(root):
        if dirs:
            return dirs
def gen_data():
    dirs = get_data_object()
    random.shuffle(dirs)
    for i in range(len(dirs)):
        patient_id = dirs[i]
        if i < 12:
            model = "train"
        elif i < 14:
            model = "val"
        else:
            model = "test"

        patient_path = os.path.join(DATA_ROOT,patient_id)
        gt,img = get_T1_filename(patient_path)
        for j in range(len(gt)):
            output = os.path.join(PATH,MODEL,model,"GT","Subj_"+str(i)+"slice_"+str(j+1)+".png")
            shutil.copy(gt[j],output)

        for j in range(len(img)):
            output = os.path.join(PATH,MODEL,model,"Img","Subj_"+str(i)+"slice_"+str(j+1)+".dcm")
            shutil.copy(img[j],output)

def dcm_to_png(model = "train"):
    assert model in ["train","val","test"]
    data_dirs = os.path.join(PATH,MODEL,model)
    data_name = os.listdir(data_dirs)


gen_data()
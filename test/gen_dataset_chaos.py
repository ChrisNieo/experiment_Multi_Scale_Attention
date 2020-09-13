import os
import random
import shutil
import pydicom
from skimage import img_as_float
import matplotlib.pyplot as plt
import cv2 as cv
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
            output = os.path.join(PATH,MODEL,model,"GT_Whole","Subj_"+patient_id+"slice_"+str(j+1)+".png")
            shutil.copy(gt[j],output)

        for j in range(len(img)):
            output = os.path.join(PATH,MODEL,model,"DCM","Subj_"+patient_id+"slice_"+str(j+1)+".dcm")
            shutil.copy(img[j],output)

def dcm_to_png(model = "train"):
    assert model in ["train","val","test"]
    data_dirs = os.path.join(PATH,MODEL,model,"DCM")
    data_names = os.listdir(data_dirs)
    for i in range(len(data_names)):
        dcm_name = os.path.join(PATH,MODEL,model,"DCM",data_names[i])
        save_name = os.path.join(PATH,MODEL,model,"Img",data_names[i].split(".")[0]+".png")
        dcm = pydicom.dcmread(dcm_name)
        img_array = dcm.pixel_array
        temp = img_array.copy()
        max = img_array.max()
        vmin = img_array.min()
        vmax = temp[temp<max].max()
        img_array[img_array > vmax] = 0
        img_array[img_array < vmin] = 0
        img_array = img_as_float(img_array)
        plt.cla()
        plt.figure('adjust_gamma', figsize=(256/100, 256/100))
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        plt.imshow(img_array, 'gray')
        plt.axis('off')
        plt.savefig(save_name)

def gt_to_liver(model = "train"):
    assert model in ["train","val","test"]
    data_dirs = os.path.join(PATH,MODEL,model,"GT_Whole")
    data_names = os.listdir(data_dirs)
    for i in range(len(data_names)):
        gt_name = os.path.join(PATH,MODEL,model,"GT_Whole",data_names[i])
        save_name = os.path.join(PATH,MODEL,model,"GT",data_names[i])
        src = cv.imread(gt_name)
        for i in range(src.shape[0]):
            for j in range(src.shape[1]):
                for k in range(src.shape[2]):
                    if 55 <= src.item(i, j, k) <= 70:
                        src.itemset((i, j, k), 255)
                    else:
                        src.itemset((i, j, k), 0)
        cv.imwrite(save_name, src)

gt_to_liver(model="train")
gt_to_liver(model="test")
gt_to_liver(model="val")
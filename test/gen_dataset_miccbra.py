import os
import SimpleITK as sitk
from skimage.io import imread, imsave
import numpy as np
PATH = "../../DataSet"
MODEL = "2-MICCAI_BraTS_2018"
SOURCE = "MICCAI_BraTS_2018_Data_Training"
OUT_PUT_DIR = os.path.join(PATH,MODEL)
DATA_ROOT = os.path.join(PATH,MODEL,SOURCE)
flair_name = "_flair.nii.gz"
t1_name = "_t1.nii.gz"
t1ce_name = "_t1ce.nii.gz"
t2_name = "_t2.nii.gz"
mask_name = "_seg.nii.gz"

def get_data_object(root = DATA_ROOT,mode="HGG"):
    assert mode in ["HGG","LGG"]
    for root,dirs,files in os.walk(os.path.join(root,mode)):
        if dirs:
            return dirs

def gen_data(root = DATA_ROOT, type = "HGG",mode="train",out_put_root = OUT_PUT_DIR):
    assert mode in ["train","test","val"] and type in ["HGG","LGG"]
    dirs = get_data_object(root,type)
    for i in range(len(dirs)):
        subject = dirs[i];
        sub_path = os.path.join(DATA_ROOT,type,subject)
        flair_img = os.path.join(sub_path,subject+flair_name)
        t1_img = os.path.join(sub_path,subject+t1_name)
        t1ce_img = os.path.join(sub_path,subject+t1ce_name)
        t2_img = os.path.join(sub_path,subject+t2_name)
        mask_img = os.path.join(sub_path,subject+mask_name)
        flair = sitk.ReadImage(flair_img,sitk.sitkInt16)
        flair_arr = sitk.GetArrayFromImage(flair)
        mask = sitk.ReadImage(mask_img,sitk.sitkInt8)
        mask_arr = sitk.GetArrayFromImage(mask)
        #flair_arr = np.array(flair_arr,dtype=np.int16)
        for j in range(len(flair_arr)):
            img_slice = flair_arr[j]
            img_name = os.path.join(out_put_root,mode,"Img","Subj_"+dirs[i]+"slice"+"_"+str(j))+".png"
            gt_slice = mask_arr[j]
            gt_name = os.path.join(out_put_root,mode,"GT","Subj_"+dirs[i]+"slice"+"_"+str(j))+".png"
            imsave(img_name,img_slice)
            imsave(gt_name,gt_slice)
        break

gen_data()
# for root,dirs,files in os.walk(DATA_ROOT):
#     print(dirs)


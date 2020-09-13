import torch
import os
import cv2 as cv
root = "../../DataSet/Chaos_Challenge/train/GT"
img_names = os.listdir(root)
for name in img_names:
    img = cv.imread(os.path.join(root,name))
    if  not img.shape[0] == 256 :
        print(name)
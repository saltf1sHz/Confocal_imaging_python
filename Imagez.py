# coding=utf-8
# confocal imaging by saltfish
# need to use file like *data1.dat *data2.dat *data3.dat
# output data has been delete the first column and remove the lightpot

# import Libaray
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2

# Find the currrent path
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
subfolder_names = os.listdir(current_dir)
# enter the current folder
for subfolder_name in subfolder_names:
    # obtain the subfolder_path
    subfolder_path = os.path.join(current_dir, subfolder_name)
    if not os.path.isdir(subfolder_path):
        continue
    os.chdir(subfolder_path)
    files = os.listdir('./')
    # choose the dat files and obtain the name
    for i in files:
        if i[-4:] == '.dat' and 'data' in i :
            filename = os.path.splitext(i)[0]
            # load the raw matrix via pandas
            rawdata = pd.read_csv(i, index_col=False, header=None).iloc[:,:-1]
            rawdata = rawdata.astype(np.uint16)
            
            rawdata = (rawdata - rawdata.min()) / (rawdata.max() - rawdata.min()) * 255.0
            plt.imshow(rawdata, cmap='gray')
            plt.show()

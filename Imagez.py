# coding=utf-8
# confocal imaging by saltfish
# need to use file like *data1.dat *data2.dat *data3.dat
# output data has been delete the first column and remove the lightpot

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
            nprawdata = rawdata.values.astype(np.uint8)
            npdata = np.delete(nprawdata, [-1,-2], axis=1)
            dealdata = cv2.resize(npdata, (1000, 1000))
            # medianBlurfilter to limte the nosie
            dealdata = cv2.medianBlur(dealdata, 3)
            # gaussianfilter to limte the nosie
            ## dealdata = cv2.GaussianBlur(nprawdata, (3,3), 0)
            # Generate sharpen core
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            dealdata = cv2.filter2D(dealdata, -5, kernel)
            # Histogram Equalization 
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            dealdata = clahe.apply(dealdata)
            if dealdata.max() - dealdata.min() == 0:
            # if range is zero, set all values to zero
                Adata = np.zeros((1000, 1000), dtype=np.uint8)
            else:
                Adata = (dealdata - dealdata.min()) / (dealdata.max() -dealdata.min()) * 255.0
                Bdata = cv2.resize(Adata, (1000, 1000))
                a = np.zeros((1000, 1000), dtype=np.uint8)
                # save npy files as temp, maybe dont need
                np.save(filename, Bdata)
    newfiles = os.listdir('./')
    combined_image = np.zeros((1000, 1000, 3), dtype=np.uint8)
    for i in newfiles:
        # load three chanel
        if i[-4:] == '.npy':
                    filename = os.path.splitext(i)[0]
                    if filename.find('data1') != -1:
                        red_channel = np.load(i)
                        cv2.imwrite('561.tiff', np.uint8(red_channel))
                        combined_image[:, :, 0] = red_channel
                    elif filename.find('data2') != -1:
                        green_channel = np.load(i)
                        cv2.imwrite('488.tiff', np.uint8(green_channel))
                        combined_image[:, :, 1] = green_channel
                    elif filename.find('data3') != -1:
                        blue_channel = np.load(i)
                        cv2.imwrite('640.tiff', np.uint8(blue_channel))
                        combined_image[:, :, 2] = blue_channel
    plt.imshow(combined_image)
    plt.title('Combined Image')
    plt.axis('off')
    plt.show()

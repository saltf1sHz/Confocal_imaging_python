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
from scipy import ndimage
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ttkbootstrap.constants import *

def load_Data(directory):
        os.chdir(directory)
        files = os.listdir('./')
        # choose the dat files and obtain the name
        for i in files:
            if i[-4:] == '.dat' and 'data' in i :
                filename = os.path.splitext(i)[0]
                 # load the raw matrix via pandas
                rawdata = pd.read_csv(i, index_col=False, header=None).iloc[:,:-1]
                nprawdata = rawdata.values.astype(np.int64)
                dealdata = np.delete(nprawdata, [-1,-2], axis=1)
                # medianBlurfilter to limte the nosie
                dealdata = ndimage.median_filter(dealdata, size=3)
                Tdata = dealdata / dealdata.max() * 255
                dealdata = Tdata.astype(np.uint8)
                # Histogram Equalization 
                clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(32,32))
                dealdata = clahe.apply(dealdata)
                if dealdata.max() - dealdata.min() == 0:
                # if range is zero, set all values to zero
                    Adata = np.zeros((1000, 1000))
                    np.save(filename, Adata)
                else:
                    Bdata = cv2.resize(dealdata, (1000, 1000))
                    a = np.zeros((1000, 1000))
                    # save npy files as temp, maybe dont need
                    np.save(filename, Bdata)

def draw_Image(directory):      
    os.chdir(directory)
    files = os.listdir('./') 
    fig = plt.figure(figsize=(720/100, 720/100), dpi=300)
    combined_image = np.zeros((1000, 1000, 3), dtype=np.uint8 )
    for i in files:
        # load three chanel and save tiff
        if i[-4:] == '.npy':
                    print(i)
                    filename = os.path.splitext(i)[0]
                    if filename.find('data1') != -1:
                        red_channel = np.load(i)
                        cv2.imwrite('561.tiff', (red_channel))
                        combined_image[:, :, 2] = red_channel
                    elif filename.find('data2') != -1:
                        green_channel = np.load(i)
                        cv2.imwrite('488.tiff', (green_channel))
                        combined_image[:, :, 1] = green_channel
                    elif filename.find('data3') != -1:
                        blue_channel = np.load(i)
                        cv2.imwrite('640.tiff', (blue_channel))
                        combined_image[:, :, 0] = blue_channel
    cv2.imwrite('Merge.tiff', combined_image)
    redimg = red_channel
    grnimg = green_channel
    bludimg = blue_channel
    mrgimg = cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB)
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    cmap = 'gray'
    axs[0, 1].imshow(redimg, cmap=cmap)
    axs[0, 1].set_title('Red Chanel')
    axs[0, 0].imshow(grnimg, cmap=cmap)
    axs[0, 0].set_title('Green Chanel')
    axs[1, 0].imshow(bludimg, cmap=cmap)
    axs[1, 0].set_title('Blue Chanel')
    axs[1, 1].imshow(mrgimg)
    axs[1, 1].set_title('Merge Chanel')
    for i in directory:
                if i[-4:] == '.npy':
                    os.remove(i)
    if 'canvas1' in globals():
        # if canvas exists, destroy it
        canvas1.get_tk_widget().destroy()
        for widget in root.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg) or isinstance(widget, NavigationToolbar2Tk):
                widget.destroy()
        
    # Create new canvas
    canvas1 = FigureCanvasTkAgg(fig, master=main_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=0)

    toolbar = NavigationToolbar2Tk(canvas1, main_frame)
    toolbar.update()
    canvas1.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=0)

    # Avoid the blink of polt window
    plt.close('all')


    fig.tight_layout(pad=2)
    plt.show()
 


def select_directory():
    directory = filedialog.askdirectory()
    load_Data(directory)
    draw_Image(directory)

root = ttk.Window()
style = ttk.Style("vapor")
root.title("Imaging")
root.geometry("1080x880")

# create frame for files
firstline_frame = ttk.Frame(root, width=720, height=80)
firstline_frame.pack(side=ttk.TOP, fill=ttk.BOTH)

load_button = ttk.Button(firstline_frame, text="Choose the DATA path", command=select_directory)
load_button.pack(side=ttk.LEFT)

cb_autogreen = ttk.BooleanVar()
cb_autogreen.set(True)
greenautobutton = ttk.Checkbutton(firstline_frame, bootstyle="round-toggle", text="Green Auto", variable=cb_autogreen)
greenautobutton.pack(side=ttk.LEFT, padx=5)

greenscale = ttk.Scale(
master=firstline_frame,
orient=HORIZONTAL,
value=75,
from_=0,
to=100
).pack(side=ttk.LEFT, padx=5)

greentxt = ttk.Entry(firstline_frame, show=None, width=6)
greentxt.insert('0',"Def")
greentxt.pack(side=ttk.LEFT, padx=5)

cb_autored = ttk.BooleanVar()
cb_autored.set(True)
redautobutton = ttk.Checkbutton(firstline_frame, bootstyle="round-toggle", text="Red Auto", variable=cb_autored)
redautobutton.pack(side=ttk.LEFT, padx=5)

redscale = ttk.Scale(
master=firstline_frame,
orient=HORIZONTAL,
value=75,
from_=0,
to=100
).pack(side=ttk.LEFT, padx=5)


cb_autoblue = ttk.BooleanVar()
cb_autoblue.set(True)
blueautobutton = ttk.Checkbutton(firstline_frame, bootstyle="round-toggle", text="Blue Auto", variable=cb_autoblue)
blueautobutton.pack(side=ttk.LEFT, padx=5)

bluescale = ttk.Scale(
master=firstline_frame,
orient=HORIZONTAL,
value=75,
from_=0,
to=100
).pack(side=ttk.LEFT, padx=5)


main_frame = ttk.Frame(root,width=720, height=720)
main_frame.pack(side=ttk.TOP, fill=ttk.BOTH)

root.mainloop()

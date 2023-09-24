PATHTOFILE = "C:\\Users\\dawid\Desktop\\Json_Pyton\\Motor_Data\\"
MOTORSTATE = "Broken_Prop"
PATHTORESULTIMAGE = f"{PATHTOFILE}\{MOTORSTATE}"
IaFile = open(f"{PATHTORESULTIMAGE}Ia.txt","a+")
IbFile = open(f"{PATHTORESULTIMAGE}Ib.txt","a+")
IcFile = open(f"{PATHTORESULTIMAGE}Ic.txt","a+")
AxFile = open(f"{PATHTORESULTIMAGE}Ax.txt","r")
AyFile = open(f"{PATHTORESULTIMAGE}Ay.txt","r")
AzFile = open(f"{PATHTORESULTIMAGE}Az.txt","r")
GxFile = open(f"{PATHTORESULTIMAGE}Gx.txt","r")
GyFile = open(f"{PATHTORESULTIMAGE}Gy.txt","r")
GzFile = open(f"{PATHTORESULTIMAGE}Gz.txt","r")
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np
import math
import time
from scipy import signal as sp 
import os 
from scipy.fft import rfft, rfftfreq
from colormap import Colormap
from PIL import Image
Ax = []
Az = []
Ay = []
AxResult = []
AyResult = []
AzResult = []
iteration = 0
cm = Colormap()
my_cmap_red = cm.cmap_bicolor('black', 'red')
my_cmap_green = cm.cmap_bicolor('black', 'green')
my_cmap_blue = cm.cmap_bicolor('black', 'blue')
GYRO_RESOLUTION = 131.00
ACC_RESOLUTION =  16384.00
BUFFOR_LEN = 19312
iteration = 0
Ax = []
Ay = []
Az = []
Gx = []
Gy = []
Gz = []




def SDFT(param1,param2,param3,name):
    global iteration
    plt.figure(2)
    plt.figure(3)
    plt.figure(4)
    PATHTOFILE = "C:\\Users\\dawid\\Desktop\\Json_Pyton\\Motor_Data\\"
    MOTORSTATE = "IMU\\Broken_Prop"
    PATHTORESULTIMAGE = f"{PATHTOFILE}\\{MOTORSTATE}\\"

    window_length = len(param1);
    window = np.hamming(window_length);
    signal = param1
    fs = 500


    #window = np.kaiser(window_length,5);
    overlap = math.floor(window_length-1);
    fft_length = window_length*2;
    stft_frequency, stft_time, signal_stft = sp.stft(signal,fs=fs,window=window,nperseg=window_length,noverlap=overlap,nfft=fft_length,return_onesided=False);
    signal_stft = signal_stft[0:window_length-1,:];
    stft_frequency = stft_frequency[0:window_length-1];
    signal_stft_abs = abs(signal_stft);
    
    fig2 = plt.figure(2)
    plt.pcolormesh(stft_time, stft_frequency, signal_stft_abs, shading='nearest', cmap = my_cmap_green);
    plt.plot()
    fig2.canvas.draw()
    data2 = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
    data2 = data2.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
    data2 = data2[58:428,80:577,:]

    signal = param2
    fs = 500


    #window = np.kaiser(window_length,5);
    overlap = math.floor(window_length-1);
    fft_length = window_length*2;
    stft_frequency, stft_time, signal_stft = sp.stft(signal,fs=fs,window=window,nperseg=window_length,noverlap=overlap,nfft=fft_length,return_onesided=False);
    signal_stft = signal_stft[0:window_length-1,:];
    stft_frequency = stft_frequency[0:window_length-1];
    signal_stft_abs = abs(signal_stft);
    
    fig3 = plt.figure(3);
    plt.pcolormesh(stft_time, stft_frequency, signal_stft_abs, shading='nearest', cmap = my_cmap_blue);
  
    fig3.canvas.draw()
    data3 = np.frombuffer(fig3.canvas.tostring_rgb(), dtype=np.uint8)
    data3 = data3.reshape(fig3.canvas.get_width_height()[::-1] + (3,))
    data3 = data3[58:428,80:577,:]


        
    signal = param3
    fs = 500

    overlap = math.floor(window_length-1);
    fft_length = window_length*2;
    stft_frequency, stft_time, signal_stft = sp.stft(signal,fs=fs,window=window,nperseg=window_length,noverlap=overlap,nfft=fft_length,return_onesided=False);
    signal_stft = signal_stft[0:window_length-1,:];
    stft_frequency = stft_frequency[0:window_length-1];
    signal_stft_abs = abs(signal_stft);

    fig4 = plt.figure(4);
    plt.pcolormesh(stft_time, stft_frequency, signal_stft_abs, shading='nearest', cmap = my_cmap_red);
    plt.plot()
    fig4.canvas.draw()
    data4 = np.frombuffer(fig4.canvas.tostring_rgb(), dtype=np.uint8)
    data4 = data4.reshape(fig4.canvas.get_width_height()[::-1] + (3,))
    data4 = data4[58:428,80:577,:]
    plt.show()
    datargb = data2 + data3 + data4
    im = Image.fromarray(datargb)

    im.thumbnail((128,64))
    if name == "Acc":
        accimg = im
    elif name == "Gyro":
        gyroimg = im
    
    #ImageFinal = Image.new("RGB",(64,128),"white")
    #ImageFinal = accimg
    #ImageFinal.paste(self.accimg,(0,0))
    #ImageFinal.paste(self.gyroimg,(0,64))
    im.save(f"{PATHTORESULTIMAGE}{iteration}.png")
    im.show()






for i in range(0,10):
    Ax = []
    Ay = []
    Az = []
    for i in range (0,26):

        AxResult = AxFile.readline()
        AxResult = AxResult[1:-2]
        one,two,three,four,five,six,seven,eigh = AxResult.split(', ')
        Ax.append(float(one))
        Ax.append(float(two))
        Ax.append(float(three))
        Ax.append(float(four))
        Ax.append(float(five))
        Ax.append(float(six))
        Ax.append(float(seven))
        Ax.append(float(eigh))
    for i in range (0,26):
        AzResult = AzFile.readline()
        AzResult = AzResult[1:-2]
        one,two,three,four,five,six,seven,eigh = AzResult.split(', ')
        Az.append(float(one))
        Az.append(float(two))
        Az.append(float(three))
        Az.append(float(four))
        Az.append(float(five))
        Az.append(float(six))
        Az.append(float(seven))
        Az.append(float(eigh))
    for i in range (0,26):
        AyResult = AyFile.readline()
        AyResult = AyResult[1:-2]
        one,two,three,four,five,six,seven,eigh = AyResult.split(', ')
        Ay.append(float(one))
        Ay.append(float(two))
        Ay.append(float(three))
        Ay.append(float(four))
        Ay.append(float(five))
        Ay.append(float(six))
        Ay.append(float(seven))
        Ay.append(float(eigh))
    Ax = butter_highpass_filter(Ax, cutoff, fs, order)
    Ay = butter_highpass_filter(Ay, cutoff, fs, order)
    Az = butter_highpass_filter(Az, cutoff, fs, order)
    SDFT(Ax,Ay,Az,"Acc")
    iteration = iteration+1




from scipy.fft import rfft, rfftfreq
from colormap import Colormap
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import math
from scipy import signal as sp 
from multiprocessing import Process
samples = []
imusamples = []
for i in range(0,258):
    imusamples.append(i)
for i in range(0,3200):
     samples.append(i)
bufforlen = 9602
class  ProcessIMUData:


    

    def __init__(self,Ax,Ay,Az,Gx,Gy,Gz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Gx = Gx
        self.Gy = Gy
        self.Gz = Gz
    GYRO_RESOLUTION = 131.00
    ACC_RESOLUTION =  16384.00
    BUFFOR_LEN = 19312
    iteration = 0
    tempiter = -1
    PATHTOFILE = "C:\\Users\\dawid\Desktop\\Json_Pyton\\Motor_Data"
    MOTORSTATE = "IMU\\Broken_Prop"
    PATHTORESULTIMAGE = f"{PATHTOFILE}\\{MOTORSTATE}\\"

    SAVEPREV = False
    prevAx = []
    prevAy = []
    prevAz = []
    prevGx = []
    prevGy = []
    prevGz = []
    cm = Colormap()

    my_cmap_red = cm.cmap_bicolor('black', 'red')
    my_cmap_green = cm.cmap_bicolor('black', 'green')
    my_cmap_blue = cm.cmap_bicolor('black', 'blue')
    accimg = 0
    gyroimg = 0

    def SDFT(self,param1,param2,param3,name):
        
        window_length = len(param1);
        window = np.hamming(window_length);
        signal = param1
        fs = 200


        #window = np.kaiser(window_length,5);
        overlap = math.floor(window_length-1);
        fft_length = window_length*2;
        stft_frequency, stft_time, signal_stft = sp.stft(signal,fs=fs,window=window,nperseg=window_length,noverlap=overlap,nfft=fft_length,return_onesided=False);
        signal_stft = signal_stft[0:window_length-1,:];
        stft_frequency = stft_frequency[0:window_length-1];
        signal_stft_abs = abs(signal_stft);


        plt.figure(2);
        
        plt.grid(None)
        figure_STFT_Gy = plt.pcolormesh(stft_time, stft_frequency, signal_stft_abs, shading='nearest', cmap = self.my_cmap_green);
        fig2 = plt.figure(2);
        fig2.canvas.draw()
        data2 = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
        data2 = data2.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
        data2 = data2[58:428,80:577,:]

        signal = param2
        fs = 200


        #window = np.kaiser(window_length,5);
        overlap = math.floor(window_length-1);
        fft_length = window_length*2;
        stft_frequency, stft_time, signal_stft = sp.stft(signal,fs=fs,window=window,nperseg=window_length,noverlap=overlap,nfft=fft_length,return_onesided=False);
        signal_stft = signal_stft[0:window_length-1,:];
        stft_frequency = stft_frequency[0:window_length-1];
        signal_stft_abs = abs(signal_stft);

        plt.figure(3);
        figure_STFT_Gz = plt.pcolormesh(stft_time, stft_frequency, signal_stft_abs, shading='nearest', cmap = self.my_cmap_blue);
        fig3 = plt.figure(3);
        fig3.canvas.draw()
        data3 = np.frombuffer(fig3.canvas.tostring_rgb(), dtype=np.uint8)
        data3 = data3.reshape(fig3.canvas.get_width_height()[::-1] + (3,))
        data3 = data3[58:428,80:577,:]

        im = plt.figure(3)
            
        signal = param3
        fs = 200


        #window = np.kaiser(window_length,5);
        overlap = math.floor(window_length-1);
        fft_length = window_length*2;
        stft_frequency, stft_time, signal_stft = sp.stft(signal,fs=fs,window=window,nperseg=window_length,noverlap=overlap,nfft=fft_length,return_onesided=False);
        signal_stft = signal_stft[0:window_length-1,:];
        stft_frequency = stft_frequency[0:window_length-1];
        signal_stft_abs = abs(signal_stft);

        plt.figure(4);
        figure_STFT_Gx = plt.pcolormesh(stft_time, stft_frequency, signal_stft_abs, shading='nearest', cmap = self.my_cmap_red);
        fig4 = plt.figure(4);
        fig4.canvas.draw()
        data4 = np.frombuffer(fig4.canvas.tostring_rgb(), dtype=np.uint8)
        data4 = data4.reshape(fig4.canvas.get_width_height()[::-1] + (3,))
        data4 = data4[58:428,80:577,:]
        
        datargb = data2 + data3 + data4
        im = Image.fromarray(datargb)

        im.thumbnail((128,64))
        if name == "Acc":
            self.accimg = im
        elif name == "Gyro":
            self.gyroimg = im

        param1.clear()
        param2.clear()
        param3.clear()
    StartSDFT =  0 
    def MakeSDFT(self):
        self.SDFT(self.Ax,self.Ay,self.Az,"Acc")
        self.SDFT(self.Gx,self.Gy,self.Gz,"Gyro")
        ImageFinal = Image.new("RGB",(64,128),"white")
        ImageFinal.paste(self.accimg,(0,0))
        ImageFinal.paste(self.gyroimg,(0,64))
        ImageFinal.save(f"{self.PATHTORESULTIMAGE}{self.iteration}.png")
        self.StartSDFT.join()

    StartSDFT = Process(target=MakeSDFT)


    def on_message(self,client, userdata, message):
        CurrentList = []
        ia = []
        ib = []
        ic = []

        for i in range(0,self.BUFFOR_LEN,2):
            
            y  = i+2
            CurrentList.append((int.from_bytes(message.payload[i:y], "little")))

        plt.figure(1)

        for i in CurrentList[9603:9611]:
            self.Gx.append(float(i)/self.GYRO_RESOLUTION)
        for i in CurrentList[9612:9620]:
            self.Gy.append(float(i)/self.GYRO_RESOLUTION)
        for i in CurrentList[9621:9629]:
            self.Gz.append(float(i)/self.GYRO_RESOLUTION)
        for i in CurrentList[9630:9638]:
            self.Ax.append(float(i)/self.ACC_RESOLUTION)
        for i in CurrentList[9639:9647]:
            self.Ay.append(float(i)/self.ACC_RESOLUTION)
        for i in CurrentList[9648:]:
            self.Az.append(float(i)/self.ACC_RESOLUTION)

        if (len(self.Gz)>128):
            self.iteration = self.iteration+1
            self.StartSDFT.start()
            self.StartSDFT.join()
            """
            
            if self.iteration ==  1:  

                self.prevGx.append(self.Gx[-33:-1])
                self.prevAx.append(self.Ax[-33:-1])
                self.prevGy.append(self.Gy[-33:-1])
                self.prevAy.append(self.Ay[-33:-1]) 
                self.prevGz.append(self.Gz[-33:-1])
                self.prevAz.append(self.Az[-33:-1])
            if self.iteration >=2 :
                for i in range(0,32):
                    self.tempiter += 1   
                    self.Gx.insert(self.tempiter,self.prevGx[0][i])
                    self.Gy.insert(self.tempiter,self.prevGy[0][i])
                    self.Gz.insert(self.tempiter,self.prevGz[0][i]) 
                    self.Ax.insert(self.tempiter,self.prevAx[0][i]) 
                    self.Ay.insert(self.tempiter,self.prevAy[0][i])
                    self.Az.insert(self.tempiter,self.prevAz[0][i])
                self.prevGx.clear()
                self.prevGz.clear()
                self.prevGy.clear()
                self.prevAx.clear()
                self.prevAy.clear()
                self.prevAz.clear()
                self.prevGx.append(self.Gx[-33:-1])
                self.prevAx.append(self.Ax[-33:-1])
                self.prevGy.append(self.Gy[-33:-1]) 
                self.prevAy.append(self.Ay[-33:-1]) 
                self.prevGz.append(self.Gz[-33:-1])
                self.prevAz.append(self.Az[-33:-1])
            self.tempiter = -1
            """

        """            self.SDFT(self.Ax,self.Ay,self.Az,"Acc")
                    self.SDFT(self.Gx,self.Gy,self.Gz,"Gyro")
                    ImageFinal = Image.new("RGB",(64,128),"white")
                    ImageFinal.paste(self.accimg,(0,0))
                    ImageFinal.paste(self.gyroimg,(0,64))
                    ImageFinal.save(f"{self.PATHTORESULTIMAGE}{self.iteration}.png")"""
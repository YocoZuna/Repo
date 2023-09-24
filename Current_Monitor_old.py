import paho.mqtt.client as mqtt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd 
from scipy import signal as sp 
import math
import os 
from scipy.fft import rfft, rfftfreq
import numpy as np
from scipy.signal import butter, lfilter, freqz
from colormap import Colormap
from PIL import Image

from matplotlib import pyplot as plt
samples = []
imusamples = []
for i in range(0,129):
    imusamples.append(i)
for i in range(0,3200):
     samples.append(i)
bufforlen = 9602
GYRO_RESEOLUTION = 131.00
ACC_RESOLUTION =  16384.00


class Moving_Avgr_Filter:


    def __init__(self):
   
        
        self.moving_coeff = []
        
        
        for i in range(0,100):
            self.moving_coeff.append(0.1)
    
        self.buff = []
        for y in range(0,len(self.moving_coeff)):
            self.buff.append(0.0) 
        self.buffIndex = 0
        self.out = 0

    def Filter_Fill(self,input):
        

        # Store latest sample in buffer
        self.buff[self.buffIndex] = input

        #Increment buffer index and wrap around if necessary

        self.buffIndex = self.buffIndex+1

        if self.buffIndex == len(self.moving_coeff):
            self.buffIndex = 0 
       
        self.out = 0

        self.sumIndex = self.buffIndex

        for n in range(0,len(self.moving_coeff)):

            if self.sumIndex > 0:
                self.sumIndex = self.sumIndex-1
            else:
                self.sumIndex = len(self.moving_coeff)-1

            self.temp1 = float(self.moving_coeff[n])
            self.temp2 = float(self.buff[self.sumIndex])

            self.out = self.out + self.temp1 * self.temp2
        return float(self.out)
MovingFiltr = Moving_Avgr_Filter()

class  Mqtt:
    cm = Colormap()
    iteration = 0

    PATHTOFILE = "C:\\Users\\dawid\Desktop\\Json_Pyton\\Motor_Data"
    MOTORSTATE = "Current\\Broken_Prop"
    PATHTORESULTIMAGE = f"{PATHTOFILE}\\{MOTORSTATE}\\"
    iteration = 0
    current_image = 0
    BUFFOR_LEN = 19312
    def CreateImage(self,pa_RGB,pb_RGB,pc_RGB):
        minima = np.min(pa_RGB)
        pa_RGB = [x - minima for x in pa_RGB]
        maxima = np.max(pa_RGB)
        pa_RGB = [x * (400/maxima) for x in pa_RGB]

        minima = np.min(pb_RGB)
        pb_RGB = [x - minima for x in pb_RGB]
        maxima = np.max(pb_RGB)
        pb_RGB = [x * (400/maxima) for x in pb_RGB]

        minima = np.min(pc_RGB)
        pc_RGB = [x - minima for x in pc_RGB]
        maxima = np.max(pc_RGB)
        pc_RGB = [x * (400/maxima) for x in pc_RGB]
        for i in range(0,len(pa_RGB)):
            pa_RGB[i] = int(np.round(pa_RGB[i]))
            pb_RGB[i] = int(np.round(pb_RGB[i]))
            pc_RGB[i] = int(np.round(pc_RGB[i]))

        for i in range(0,2800):
            self.current_image = self.current_image+1
            pa_temp = pa_RGB[i:i+400]
            pb_temp = pb_RGB[i:i+400]
            pc_temp = pc_RGB[i:i+400]
            add_zeros_pa = 0
            add_zeros_pb = 1
            add_zeros_pc = 1
            for i in range(0, len(pa_RGB)):
                pa_temp.insert(add_zeros_pa+1, 0)
                pa_temp.insert(add_zeros_pa+2, 0)
                add_zeros_pa = add_zeros_pa + 3

            for i in range(0, len(pb_RGB)):
                pb_temp.insert(add_zeros_pb-1, 0)
                pb_temp.insert(add_zeros_pb+1, 0)
                add_zeros_pb = add_zeros_pb + 3

            for i in range(0, len(pc_RGB)):
                pc_temp.insert(add_zeros_pc-1, 0)
                pc_temp.insert(add_zeros_pc-1, 0)
                add_zeros_pc = add_zeros_pc + 3

        
            pa_temp1 = np.asarray(pa_temp)
            pa_temp1 = pa_temp1.astype(np.uint8)
            pa_temp1 = np.resize(pa_temp1, (16,16,3))

            pb_temp1 = np.asarray(pb_temp)
            pb_temp1 = pb_temp1.astype(np.uint8)
            pb_temp1 = np.resize(pb_temp1, (16,16,3))

            pc_temp1 = np.asarray(pc_temp)
            pc_temp1 = pc_temp1.astype(np.uint8)
            pc_temp1 = np.resize(pc_temp1, (16,16,3))



            imr = Image.fromarray(pa_temp1)
            img = Image.fromarray(pb_temp1)
            imb = Image.fromarray(pc_temp1)
            finalimg = pa_temp1+pb_temp1+pc_temp1

            final = Image.fromarray(finalimg)
            final.save(f"{self.PATHTORESULTIMAGE}{self.current_image}.png")
            
            pa_temp.clear()
            pb_temp.clear()
            pc_temp.clear()
            
        

    def on_message(self,client, userdata, message):
        CurrentList = []
        ia = []
        ib = []
        ic = []

        self.iteration = self.iteration+1
        for i in range(0,self.BUFFOR_LEN,2):
            y  = i+2
            CurrentList.append((int.from_bytes(message.payload[i:y], "little")))

        plt.figure(1)
        ##plt.figure(2)        
        ################################ Applying moving filter
        for i in CurrentList[0:3200]:
            a = i
            ia.append(MovingFiltr.Filter_Fill(a))
        for i in CurrentList[3201:6401]:
            b= i
            ib.append(MovingFiltr.Filter_Fill(b))
        for i in CurrentList[6402:9602]:
            c= i
            ic.append(MovingFiltr.Filter_Fill(c))
        #Gyro
        

        self.CreateImage(ia,ib,ic)



        ia.clear()
        ib.clear()
        ic.clear()
        CurrentList.clear()
        plt.figure(1).clear()
Callback = Mqtt()
mqttBroker ="localhost"

client = mqtt.Client("CurrentMonitor")
client.connect(mqttBroker) 
client.subscribe("Motor")
client.loop_start()
while 1:
    
    client.on_message=Callback.on_message
    

client.loop_stop()
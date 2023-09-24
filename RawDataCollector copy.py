import paho.mqtt.client as mqtt
import time
import multiprocessing as mp 
class  Mqtt:
    iteration = 0
    GYRO_RESOLUTION = 131.00
    ACC_RESOLUTION =  16384.00
    BUFFOR_LEN = 19312



    def on_message(self,client, userdata, message):
        CurrentList = []
        ia = []
        ib = []
        ic = []
        Ax = []
        Ay = []
        Az = []
        Gx = []
        Gy = []
        Gz = []

        DataBufor = [ia,ib,ic,Ax,Ay,Az,Gx,Gy,Gz]
        self.iteration = self.iteration+1
        # Decoding data
        for i in range(0,self.BUFFOR_LEN,2):
            y  = i+2
            CurrentList.append((int.from_bytes(message.payload[i:y], "little")))
        #Currents
        for i in CurrentList[0:3200]:
            a = i
            ia.append(a)
            
        for i in CurrentList[3201:6401]:
            b= i
            ib.append(b)
        for i in CurrentList[6402:9602]:
            c= i
            ic.append(c)
        #Gyro
        for i in CurrentList[9603:9611]:
            Gx.append(float(i)/self.GYRO_RESOLUTION)
        for i in CurrentList[9612:9620]:
            Gy.append(float(i)/self.GYRO_RESOLUTION)
        for i in CurrentList[9621:9629]:
            Gz.append(float(i)/self.GYRO_RESOLUTION)
        for i in CurrentList[9630:9638]:
            Ax.append(float(i)/self.ACC_RESOLUTION)
        for i in CurrentList[9639:9647]:
            Ay.append(float(i)/self.ACC_RESOLUTION)
        for i in CurrentList[9648:]:
            Az.append(float(i)/self.ACC_RESOLUTION)

        """Writing data to .txt files """
        IaFile.write(str(ia)+"\n")
        IbFile.write(str(ib)+"\n")
        IcFile.write(str(ic)+"\n")
        AxFile.write(str(Ax)+"\n")
        AyFile.write(str(Ay)+"\n")
        AzFile.write(str(Az)+"\n")
        GxFile.write(str(Gx)+"\n")
        GyFile.write(str(Gy)+"\n")
        GzFile.write(str(Gz)+"\n")

PATHTOFILE = "C:\\Users\\dawid\\Desktop\\Json_Pyton\\Motor_Data"
MOTORSTATE = "RawData\\Broken_Prop"
PATHTORESULTIMAGE = f"{PATHTOFILE}\\{MOTORSTATE}\\"
IaFile = open(f"{PATHTORESULTIMAGE}Ia.txt","a+")
IbFile = open(f"{PATHTORESULTIMAGE}Ib.txt","a+")
IcFile = open(f"{PATHTORESULTIMAGE}Ic.txt","a+")
AxFile = open(f"{PATHTORESULTIMAGE}Ax.txt","a+")
AyFile = open(f"{PATHTORESULTIMAGE}Ay.txt","a+")
AzFile = open(f"{PATHTORESULTIMAGE}Az.txt","a+")
GxFile = open(f"{PATHTORESULTIMAGE}Gx.txt","a+")
GyFile = open(f"{PATHTORESULTIMAGE}Gy.txt","a+")
GzFile = open(f"{PATHTORESULTIMAGE}Gz.txt","a+")
Callback = Mqtt()
def CreateProcesWithMqtt():
    mqttBroker ="localhost"

    client = mqtt.Client("RawDataCollector")
    client.connect(mqttBroker) 
    ## Open files 

    client.subscribe("Motor")
    client.loop_start()
    while 1:
        
        client.on_message=Callback.on_message 

    client.loop_stop()
    
StartMqttInOtherProces = mp.Process(target=CreateProcesWithMqtt)
if __name__ == "__main__":
    StartMqttInOtherProces.start()
    while 1:
        continue

   

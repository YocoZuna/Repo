import os 
import random
import glob
import shutil



if os.path.isdir('Motor_Data/IMU/Broken_Prop/train') is False:
    os.makedirs('Motor_Data/IMU/Broken_Prop/train')
    os.makedirs('Motor_Data/IMU/Broken_Prop/test')
    os.chdir('Motor_Data/IMU/Broken_Prop')
    for f in random.sample(glob.glob('Broken_Prop*'),600):
        shutil.move(f,'test')
    for f in random.sample(glob.glob('Broken_Prop*'),1400):
        shutil.move(f,'train')


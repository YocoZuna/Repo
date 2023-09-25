import os 
import random
import glob
import shutil
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator


"""if os.path.isdir('Motor_Data/IMU/Broken_Prop/train') is False:
    os.makedirs('Motor_Data/IMU/Broken_Prop/train')
    os.makedirs('Motor_Data/IMU/Broken_Prop/test')
    os.chdir('Motor_Data/IMU/Broken_Prop')
    for f in random.sample(glob.glob('Broken_Prop*'),600):
        shutil.move(f,'test')
    for f in random.sample(glob.glob('Broken_Prop*'),1400):
        shutil.move(f,'train')"""

train_dataGen = ImageDataGenerator(rescale=1./255)
os.chdir('Motor_Data/IMU')
trainin_set = train_dataGen.flow_from_directory(
    directory='train',
    target_size=(128,64),
    batch_size=32,
    classes=['Broken_Prop','Healthy'])

test_dataGen = ImageDataGenerator(rescale=1./255)
test_set = test_dataGen.flow_from_directory(
    directory='test',
    target_size=(128,64),
    batch_size=32,
    classes=['Broken_Prop','Healthy'])


print(test_set.classes)
cnn = tf.keras.models.Sequential()
cnn.add(tf.keras.layers.Conv2D(filters=2,kernel_size=(4,4),activation='relu',input_shape = (128,64,3)))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=2,kernel_size=(3,3),activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=1))

cnn.add(tf.keras.layers.Conv2D(filters=32,kernel_size=(3,3),activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))
cnn.add(tf.keras.layers.Flatten())

cnn.add(tf.keras.layers.Dense(units=128,activation='relu'))

cnn.add(tf.keras.layers.Dense(units=2,activation='sigmoid'))

cnn.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])
import numpy as np
cnn.fit(x=trainin_set,validation_data=test_set,epochs=3,verbose=2)
prediction = cnn.predict(x=test_set,verbose=0)
print(np.round(prediction))
print(test_set.class_indices)

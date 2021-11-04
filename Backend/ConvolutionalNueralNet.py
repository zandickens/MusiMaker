import numpy as np
import matplotlib.pyplot as plt 
import os 
import cv2
import random
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from sklearn.preprocessing import LabelBinarizer

DataPath = "C:/Users/kmari/Documents/Senior_Project/MusiMaker/Data/images_original"
Genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

# for genre in Genres:
#     path = os.path.join(DataPath, genre)
#     for img in os.listdir(path):
#         img_array = cv2.imread(os.path.join(path,img))
#         img_array = cv2.cvtColor(img_array,cv2.COLOR_BGR2RGB)
#         plt.imshow(img_array)
#         plt.show()

training_data = []

def create_training_data():
    for genre in Genres:
        path = os.path.join(DataPath, genre)
        genre_num = Genres.index(genre)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img))
                training_data.append([img_array, genre_num])
            except Exception as e: 
                pass
create_training_data()

random.shuffle(training_data)
# for sample in training_data:
#     print(sample[1])

features = []
labels = []

for x, y in training_data:
    features.append(x)
    labels.append(y)

features = np.array(features).reshape(-1, 432, 288, 3)
labels = np.array(labels)
label_as_binary = LabelBinarizer()
train_labels = label_as_binary.fit_transform(labels)

features = features/255.0


model = tf.keras.models.Sequential()
model.add(Conv2D(64, (3,3), input_shape = features.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64, (3,3), input_shape = features.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Dense(10))
model.add(Activation('sigmoid'))

model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(features, train_labels, batch_size = 32, validation_split=0.1, epochs=10)

# model.compile(optimer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(x_train,y_train, epochs=3)

import numpy as np
import matplotlib.pyplot as plt 
import os 
import cv2
import random
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import model_from_json



DataPath = "../Data/images_original"
Genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

# Display dataset

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

#Create a new empty neural network model
def create_model():
    model = tf.keras.models.Sequential()
    model.add(Conv2D(32, (3,3), input_shape = features.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(32, (3,3), input_shape = features.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(32, (3,3), input_shape = features.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))


    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))

    model.add(Dense(10))
    model.add(Activation('relu'))

    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Create New model


model = create_model()
model.fit(features, train_labels, batch_size = 32, validation_split=0.15, epochs=20)

# Serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# Serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")


# Neural Net Optimization
# batch_size = [10, 20, 40, 60, 80, 100]
# epochs = [10, 50, 100]
#validation_split = [0.1]
# param_grid = dict(batch_size=batch_size, epochs=epochs)
# grid = GridSearchCV(estimator=model, param_grid=param_grid, verbose=1)
# grid_result = grid.fit(features, train_labels)



# #Return results of best model sizing
# print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# means = grid_result.cv_results_['mean_test_score']
# stds = grid_result.cv_results_['std_test_score']
# params = grid_result.cv_results_['params']
# for mean, stdev, param in zip(means, stds, params):
#     print("%f (%f) with: %r" % (mean, stdev, param))
# model.compile(optimer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(x_train,y_train, epochs=3)







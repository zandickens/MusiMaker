import os 
import cv2
import numpy as np
import matplotlib.pyplot as plt 
import tensorflow as tf
from keras.models import model_from_json

# LOADING A SAVED MODEL
def load_latest_model():

    json_file = open('./Backend/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("./Backend/model.h5")
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    
    # Uncomment to print accuracy when loading
    # score = loaded_model.evaluate(features, train_labels, verbose=0)
    # print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
    
    return loaded_model

#Load Model
model = load_latest_model()



#Predict

def prepImg(filepath):
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (432,288))
    return new_array.reshape(-1, 432, 288, 3)

def predict(model, filepath):
    genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
    prediction = model.predict(prepImg(filepath))
    genreIndex = np.argmax(prediction)
    return {'classification':genres[genreIndex],'confidence':list( zip( genres, list((prediction[0]/sum(prediction[0])).astype(np.float)) ) ) }
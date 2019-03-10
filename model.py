import cv2
import os
import numpy as np
from random import sample
from keras.models import model_from_json
import keras
import psutil
import easygui
import matplotlib.pyplot as plt
from keras.preprocessing import image

p = psutil.Process(os.getpid())
p.nice(19)  # set>>> p.nice()10

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

path = "/home/felipe/final_final"

from keras.models import load_model
from keras.utils.generic_utils import CustomObjectScope

with CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):

    json_file = open(path+'/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path+"/model.h5")

def predict(img):

    img = cv2.resize(img, (224,224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    preprocessed_image = keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)
    prediction = loaded_model.predict(preprocessed_image)[0]
    print(prediction)
    return prediction[2]

if __name__ == "__main__":

    pic = easygui.fileopenbox()
    pic = cv2.imread(pic)
    results = predict(pic)
    print(results)
#    plt.imshow(pic)
#    plt.show()
#




#---------------------------------------------------------------------------------

import cv2
import os
import numpy as np
from random import sample
from keras.models import model_from_json
import psutil
import easygui
import matplotlib.pyplot as plt

import keras
from keras import backend as K
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
import numpy as np
from IPython.display import Image
from keras.optimizers import Adam

p = psutil.Process(os.getpid())
p.nice(19)  # set>>> p.nice()10

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

HEIGHT = 224
WIDTH = 224

h = HEIGHT
w = WIDTH

json_file = open('model_pretrained.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_pretrained.h5")

def predict(file):
    img_path = ''
    img = image.load_img(img_path + file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    preprocessed_image = keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)
    predictions = loaded_model.predict(preprocessed_image)
    return predictions[0][1]
    
if __name__ == "__main__":

    pic = easygui.fileopenbox()
    results = predict(pic)    
    print(results)
#    plt.imshow(pic)
#    plt.show()
#




#---------------------------------------------------------------------------------

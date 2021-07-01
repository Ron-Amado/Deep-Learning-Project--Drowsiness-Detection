# -*- coding: utf-8 -*-
"""
@author: Ron Amado
"""


"""
this python file handle the classify section
"""

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display
import numpy as np
import pickle


import Prints_For_User

IMAGE_SIZE = (50,50)

class PredictImage():
    
    def __init__(self, model_path, labels_path):
        self.model_path = model_path #the path to the trained model.
        self.labels_path = labels_path #the path to the images labels.
        self.image_path = "" #the path to the image the user chose to predict.
        self.image_size= (1,1) #the size of the user's image.
        self.model = None #will contain the trained model.
        self.lb = None #will contain the images labels.
        
    def Manage_Prediction(self,image_path):
    
        """
        Get: the path to the image the user chose to predict.
        this function manage the prediction process.
        """
        
        self.load_Model()
        self.image_path = image_path
        image_arr, output = self.load_Image()
        self.predict_Image(image_arr, output)


    def load_Model(self):
        """
        load the trained convolutional neural network and the label binarizer.
        """
        Prints_For_User.printProcess("[INFO] Loading network...")
        
        self.model = load_model(self.model_path)
        self.lb = pickle.loads(open(self.labels_path, "rb").read())
    
    
    def load_Image(self):
        """
        this function load the image that the user chose to predict and prepares it for the classification process.
        the function loads the image as gray scale, converts it to numpy array, stores it in the data list 
        and scale the images pixels to range [0, 1] from range [0, 255]. (just like before the training process)
        
        return: the image numpy array and a copy of the image (before the changes)
        """
        # load the image
        image = Image.open(self.image_path)
        self.image_size= image.size
        output = image.copy()
        # pre-process the image for classification
        image = image.convert('L')
        image = image.resize(IMAGE_SIZE)
        image.save(self.image_path)
        image = np.asarray(image, 'float32')/255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        return image, output


    def predict_Image(self,image_arr, output):
        """
        Get:  the image as array and copy of the image.
        
        this method actually cllasify the image, than show the image and its label (after the classification)
        in plots.
        """
        # classify the input image
        Prints_For_User.printProcess("[INFO] Classifying image...")
        proba = self.model.predict(image_arr)[0]
        idx = np.argmax(proba)
        label = self.lb.classes_[idx]

        """
        bulid the text and draw the label on the image.
        """
        label = "{}: {:.2f}% ".format(label, proba[idx] * 100)
        output = output.resize(self.image_size)
        draw=ImageDraw.Draw(output)
        font = ImageFont.truetype("arial.ttf", size=44)
        draw.text((10,10), label, font=font, fill= "blue")
        copypath= r"C:\Users\ronam\OneDrive\שולחן העבודה\copy.jpg"
        output.save(copypath)
        
        # show the output image
        Prints_For_User.printProcess("[INFO] {}".format(label))
        display(output)
   



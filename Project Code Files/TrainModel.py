# -*- coding: utf-8 -*-
"""
@author: Ron Amado
"""

	

"""
this python file handle the train section
"""


import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
#from tensorflow.python.keras.optimizers import TFOptimizer
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from PIL import Image



import Model

import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import random
import pickle
import os

import Prints_For_User


class TrainModel():
    
    def __init__(self, dataset_path, model_path, labels_path, plot_dir):
        
        self.dataset_path = dataset_path # the data set directory
        self.model_path = model_path    # the directory where the user chose to save the trained model
        self.labels_path = labels_path #the directory where the user chose to save the images labels
        self.plot_dir = plot_dir   # the directory to the folder where the user chose to save the graph images
        
        self.EPOCHES = 20 #number of epoches
        self.INIT_LR = 1e-3  #learning rate
        self.BS = 32 #batch size
        self.IMAGE_DIMS = (50, 50, 1) #image dimensions
        self.data = []   # list of all the images as arrays
        self.labels = []  #list labels of all the images
        
        

    def manage_train(self):
    
        """
        Get: None.
        return: the train model path and the images labels path
        
        public method that manage the train section.
        """
        
        self.loading_Images()
        self.scale_Pixels()
    
        history = self.train()
    
        self.graph1(history, self.plot_dir+ r"\plot1.png")
        self.graph2(history, self.plot_dir +r"\plot2.png")
    
    
    
    def loading_Images(self):
        """
        this method load the images from the current directory, and prepares them for the training process.
        the function loads each image as gray scale, converts it to numpy array and stores it in the data list.
        in addition, the function update the Labels list.
        """
        # grab the image paths and randomly shuffle them
        Prints_For_User.printProcess("[INFO] Loading images...")
        imagePaths = sorted(list(paths.list_images(self.dataset_path)))
        random.seed(42)
        random.shuffle(imagePaths)

        # loop over the data set images
        for imagePath in imagePaths:
            """
            Prepare the images for the training process by loads each image as gray scale, converts it to numpy array
            and stores it in the data list.
            """
            image = Image.open(imagePath)           
            image = image.convert('L')
            image = image.resize((self.IMAGE_DIMS[0], self.IMAGE_DIMS[1]))
            image.save(imagePath)
            image = img_to_array(image)
            self.data.append(image)
            """
            extract the class label from the image path and update the labels list.
            """
            label = imagePath.split(os.path.sep)[-2]
            # print (label)
            self.labels.append(label)
        
 
    def scale_Pixels(self):    
        """ 
        this method scale the images pixels to range [0, 1] from range [0, 255].
        the data list store all the images by arrays so by convert this list we convert all the images pixels range.
        """
        self.data = np.array(self.data, dtype="float") / 255.0
        self.labels = np.array(self.labels)
        Prints_For_User.printProcess("[INFO] data matrix: {:.2f}MB".format(self.data.nbytes / (1024 * 1000.0)))
    
    
    
    def train(self):
    
        #binarize the labels (this is an easy tool for classification)

        lb = LabelBinarizer()
    
        #Linear transformation
        self.labels = lb.fit_transform(self.labels)

        """
        dividing the dataset to:
            70% of the data for training
            20% of the data for testing
            10% of the data for validation
        """
        
        (trainX, testX, trainY, testY) = train_test_split(self.data,
        	self.labels, test_size=0.2, random_state=42)
        (trainX, valX, trainY, valY) = train_test_split(trainX,
        	trainY, test_size=0.125, random_state=42)
     
        
        
        # construct the image generator for data augmentation
        aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	        horizontal_flip=True, fill_mode="nearest")

        
        # initialize the model
        Prints_For_User.printProcess("[INFO] Compiling model...")
        model = Model.MyModel.build(width=self.IMAGE_DIMS[1], height=self.IMAGE_DIMS[0],
	    depth= self.IMAGE_DIMS[2], classes=len(lb.classes_))
        
        opt = Adam(lr=self.INIT_LR, decay=self.INIT_LR / self.EPOCHES)
        
        model.compile(loss="categorical_crossentropy", optimizer=opt,
	        metrics=["accuracy"])
        
        model.summary()
        # train the network
        Prints_For_User.printProcess("[INFO] Training network...")
        
        H = model.fit_generator(
	    aug.flow(trainX, trainY, batch_size=self.BS),
	    validation_data=(valX, valY),
	    steps_per_epoch=len(trainX) // self.BS,
	    epochs=self.EPOCHES, verbose=2)
        

        # Evaluate the model on the test data using `evaluate`
        Prints_For_User.printProcess('\n# Evaluate on test data')
        results = model.evaluate(testX, testY, batch_size=32)
        print('test loss ' + str(results[0])  + ' , test acc ' + str(results[1]))        
        
        
        # save the model to disk
        Prints_For_User.printProcess("[INFO] Serializing network...")
        model.save(self.model_path)
    
        # save the label binarizer to disk
        Prints_For_User.printProcess("[INFO] Serializing label binarizer...")
        f = open(self.labels_path, "wb")
        f.write(pickle.dumps(lb))
        f.close()
        return H


    def graph2(self, history, plot_path):
        
        """
        Gat: the history and the path where the user chose to save the results 
        create an images that contains the graph.
        """
	    # plot loss
    
        plt.subplot(211)
        plt.title('Cross Entropy Loss')
        plt.plot(history.history['loss'], color='blue', label='train')
        plt.plot(history.history['val_loss'], color='orange', label='test')
	    # plot accuracy
        plt.subplot(212)
        plt.title('Classification Accuracy')
        plt.plot(history.history['accuracy'], color='blue', label='train')
        plt.plot(history.history['val_accuracy'], color='orange', label='test')
	    # save plot to file
        plt.savefig(plot_path)
        plt.close()
    
    
    
    def graph1(self,H, plot_path):
        """
        Gat: the history and the path where the user chose to save the results
        create an images that contains the graph.
        """
        # plot the training loss and accuracy
        plt.style.use("ggplot")
        plt.figure()
        N = self.EPOCHES
        plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
        plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="upper left")
        plt.savefig(plot_path)


   



    
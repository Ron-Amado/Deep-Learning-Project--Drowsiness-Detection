# -*- coding: utf-8 -*-
"""
@author: Ron Amado
"""


"""
this python file responsible for the MENU, the options that offered to the user.
"""
import tkinter as tk
import tkinter.font
from PIL import ImageTk, Image
import os
import Extract_ZipFile
import TrainModel
import Predict
import Propriety
import Prints_For_User


class Menu():
    
    def __init__(self):
        """
        defult directories.
        this directoties may change according to the user activity and decisions.
        """
        self.sorted_data_path = None
        #self.sorted_data_path = r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\dataset"
        self.model_path = r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\הרצות\Model.model" 
        self.labels_path = r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\הרצות\lb.pickle"



    def buttons(self):
        """
        this method responsible for the tkinter window. this window show the user the program menu,
        and manage his activity.
        there are 4 buttons->
            1. Extract zip file.
            2. Train the model
            3. Predict an image.
            4. Exit.
        if the user click on a button, this method will call the match function.
        """
        options = tk.Toplevel() 
        options.title("Ron's DL project")
        options.geometry('700x900')
        width= 300
        height= 150
         
        menu_label= tk.Label(options, text= "Hello, please pick an option!", fg='white', bg='black', width=70, height=1, font = ("Comic Sans MS", 20, "bold")).pack(pady=10)
        
        #button that will extract zip files.
        zip_image=Image.open(r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\extractzip_image.PNG")
        zip_image= zip_image.resize((width, height), Image.ANTIALIAS)
        zip_image= ImageTk.PhotoImage(zip_image)
        zip_button= tk.Button(options, image= zip_image, command=lambda: self.case_One()).pack(pady=10)
        #zip_button= tk.Button(options, text= "extract zip file", command=lambda: self.case_One(), fg= 'white', bg= 'red', width=50, height= 3).pack(pady=10)
        
        #button that will train the modal.
        train_image=Image.open(r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\train_image.PNG")
        train_image= train_image.resize((width, height), Image.ANTIALIAS)
        train_image= ImageTk.PhotoImage(train_image)
        train_button= tk.Button(options, image= train_image, command=lambda: self.case_Two()).pack(pady=10)
  
        #button that will predict an image.
        predict_image= Image.open(r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\predict_image.PNG")
        predict_image= predict_image.resize((width, height), Image.ANTIALIAS)
        predict_image= ImageTk.PhotoImage(predict_image)
        predict_button= tk.Button(options, image= predict_image, command=lambda: self.case_Three()).pack(pady=10)
 
        #button that will quit the program.
        exit_image=Image.open(r"C:\Users\ronam\OneDrive\שולחן העבודה\רון- בית ספר\Deep Learning\exitimage.png")
        exit_image= exit_image.resize((width, height), Image.ANTIALIAS)
        exit_image= ImageTk.PhotoImage(exit_image)
        exit_button= tk.Button(options, image = exit_image, command=lambda: self.close(options), bg= 'red').pack(pady= 10)

        options.mainloop()
    
    

    def case_One(self):
        """
        Get: None.
        return: None.
        
        the method inputs the dataset path from the user, and puts it in "sorted_data_path". 
        the function calls to the extract() function that located in Extract_ZipFile.py file ->
        if the path was a zip file, the program extract the files and update the class member "sorted_data_path" 
        to the path to which the files were extracted.
        if it was an ordniry path, than "sorted_data_path" doesn't change. 
                """
        
        self.sorted_data_path = Propriety.GetDirectory.is_Exsists("Please enter the full path (with the folder name) to your sorted dataset.")
        self.sorted_data_path = Extract_ZipFile.extract(self.sorted_data_path) # return the sorted dataset path after extract (if it was a zip file at first)    
        Prints_For_User.printProcess("[INFO] Using updated data set")
    


    def case_Two(self):
        """
        Get: None.
        return: None.
               
        this function inputs the path to the updated sorted dataset, the model path which will contain the trained model,
        and the labels path which will contain the label for each image.
        the function call to the manage_train() fanction that located in TrainModel.py file, and update the model path
        and the labels path.
        """
        
        if (self.sorted_data_path==None):
            self.sorted_data_path = Propriety.GetDirectory.is_Exsists("Please enter the full path (with the folder name) to your sorted dataset.")
        self.model_path = Propriety.GetDirectory.get_New_Dir("Please enter the full path (with the folder name) to the updated model. NOTE: the directiry must end with '.model'")
        self.labels_path = Propriety.GetDirectory.get_New_Dir("Please enter the full path (with the name) to output label binarizer. NOTE: the directiry must end with '.pickle' or '.txt'")
        
        while self.model_path == self.labels_path:
            Prints_For_User.printError("Error - file will be override")
            self.labels_path = Propriety.GetDirectory.get_New_Dir("Please enter again the full path (with the name) to output label binarizer. NOTE: the directiry must end with '.pickle' or '.txt'")
                
        plot_dir = Propriety.GetDirectory.get_New_Dir("Please Enter the folder directory to output accuracy/loss plot: ")
        
        while self.model_path == plot_dir or self.labels_path == plot_dir:
            Prints_For_User.printError("Error - file will be override")
            plot_dir = Propriety.GetDirectory.get_New_Dir("Please Enter the folder directory to output accuracy/loss plot: ")
    
        os.mkdir(plot_dir)
        
        train_obj = TrainModel.TrainModel(self.sorted_data_path, self.model_path, self.labels_path, plot_dir)
        
        train_obj.manage_train()
        
        Prints_For_User.printProcess("[INFO] Using trained model")
        
        

    def case_Three(self):
        """
        Get: None.
        return: None.
        
        this function inputs the path of an image. The function calls to the Manage_Prediction() fanction that 
        located in Predict.py file, and predict the image label.
        """

        image_path = Propriety.GetDirectory.is_Exsists("Please enter the image path:", True)
        predict_obj = Predict.PredictImage(self.model_path, self.labels_path)  
        predict_obj.Manage_Prediction(image_path)
        
        
          
    def close(self, options):
        """
        Get: options- the tkinter window.
        return: None.
        
        this function close the tkinter window.
        """
        Prints_For_User.printProcess("[INFO] Exiting...")
        options.destroy()
        

    
    
 

        


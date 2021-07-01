# -*- coding: utf-8 -*-
"""
@author: Ron Amado
"""


"Extract zip file"

from zipfile import ZipFile
import Propriety
import Prints_For_User

            
    
def extract(path): 
    """
    Get: the dataset path.
    return: the function check if the path is a zip file->
            if the path is zip, the function extracts the files, and returns the path to which the files were extracted.
            else (if the path is not zip), the function returns the dataset path.
    """


    check_path = path
    ls = path.split(".") 
    if ls[len(ls)-1] == "zip": #check if the file/folder is zip by its ending - ".zip" 
        Prints_For_User.printProcess("[INFO] Got a zip file...")
        check_path = Propriety.GetDirectory.get_New_Dir("Choose the path to extract the files (with a new folder name)")   

        #extract the folder to the new user's path
        with ZipFile(path, 'r') as zipObj:
            Prints_For_User.printProcess("[INFO] Extracting the images from the zip file...")
            zipObj.extractall(check_path)
        
        Prints_For_User.printProcess("[INFO] Finished extracting process.")

    else:
        Prints_For_User.printProcess("[INFO] Got ordinary file...")
    return check_path
            
            


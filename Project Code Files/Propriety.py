# -*- coding: utf-8 -*-
"""
@author: Ron Amado
"""


"""
this python file handle the input section
"""

import os
import Prints_For_User

class GetDirectory():
    
    @staticmethod
    def is_Exsists(massage):
        """
        Get: a message to print for the user (input message).
        return: an exsisting path.
        
        the function request an exsisting path from the user. It uses check_Exsists_Dir() function to check if the
        input path exsists. the function returns the input path only if it exsists (check_Exsists_Dir() returned True).
        else, this function keeps requset a path from the user.
          
            """
        Prints_For_User.printOptions(massage)
        path = input("Enter: ")

        while not GetDirectory.check_Exsists_Dir(path):
            Prints_For_User.printOptions(massage)
            path = input("Enter: ")
            
        return path
    
    
    @staticmethod
    def check_Exsists_Dir(path):
        """
        Get: a path
        return: returns True if the path exsists. else, returns False. 
        """
    
        if not os.path.exists(path):
            Prints_For_User.printError("Error - no such file or path")
            return False
    
        return True
    
    @staticmethod
    def get_New_Dir(massage):
        """
        Get: a message to print for the user (input message).
        return: a new path.
        
        the function request a new path from the user. It uses check_New_Dir() function to check if the
        input path is new and valid. the function returns the input path only if it is new and 
        valid (check_New_Dir() returned True). else, this function keeps requset a path from the user.
        """
        Prints_For_User.printOptions(massage)
        path = input("Enter: ")
    
        while not GetDirectory.check_New_Dir(path):
            Prints_For_User.printOptions(massage)
            path = input("Enter: ")
        return path 
   
    
    @staticmethod
    def check_New_Dir(path):
        """
        Get: a path
        return True if the path is new (does not exsist) and valid. else, return False.
        """
       
        if(os.path.exists(path)):
            """
            check that the path is not exisist-
            if it is, return False.
            """
            Prints_For_User.printError("Error - this path is allready exsists")
            return False
    
        try:
            """
            try to make a folder in the current path in order to check if the path proper ->
            if its succed the path is valid! -> the function returns True
            else
            the path is not vaild -> the function returns False
            """
            os.mkdir(path)
            os.rmdir(path)
            return True
         
        except:
            Prints_For_User.printError("Error - directory is not valid")            
            return False
            
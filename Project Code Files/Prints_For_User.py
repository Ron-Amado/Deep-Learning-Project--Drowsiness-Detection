# -*- coding: utf-8 -*-
"""
@author: Ron Amado
"""

"""
    this file contains the function that prints messages for the user. 
    the file prints the messages in colors:
    ->    messages in cyan- represent input messages.
    ->    messages in green- represent information messages.
    ->    messages in red- represent error messages.
"""


from colorama import init, Fore, Back, Style
    
def printError(message):
    """
    Get: message
    this method responsible for the error messages -> prints the message in red.
    """
    init(convert=True)
    print(Fore.RED + message) 
    Style.RESET_ALL
    
def printOptions(message):
    """
    Get: message
    this method responsible for the input messages -> prints the message in cyan.
    """
    init(convert=True)
    print(Fore.CYAN + message) 
    Style.RESET_ALL
        
def printProcess(message):
    """
    Get: message
    this method responsible for the information messages -> prints the message in green.
    """
    init(convert=True)
    print(Fore.GREEN + message) 
    Style.RESET_ALL
    
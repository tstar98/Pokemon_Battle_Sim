# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 14:52:38 2021

@author: Brian
"""

import tkinter as tk

# For scaling everything up/down at once
scale = 4

font = ('Arial', 8*scale)

class Default_Window(tk.Tk):
    def __init__(self, x_stretch=1, y_stretch=1):
        """Create a Tkinter window with useful settings"""
        super().__init__()
        res = [160*scale*x_stretch, 144*scale*y_stretch] # Original Game Boy Color resolution
        self.geometry(f"{res[0]}x{res[1]}")
        self.title('Pokemon Battle Simulator')
                
        # Always open in screen center
        # https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (res[0]/2)
        y = (hs/2) - (res[1]/2)
        
        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (res[0], res[1], x, y))
        
def Button(*args, **kwargs):
    """Sugar syntax to make a button using a standard set of settings"""
    kwargs.update(relief='ridge', borderwidth=1*scale, font=font)
    return tk.Button(*args, **kwargs)
    
def gridconfigure(obj, rw=None, cw=None):
    """
    Convenience function to configure the grid for a TKinter object

    Parameters
    ----------
    obj : TKinter object
        The object to configure
    rw : list, optional
        List of row weights. If None, make one row of weight 1
    cw : list, optional
        List of column weights. If None, make one column of weight 1
    """
    if rw is None:
        rw = [1]
    if cw is None:
        cw = [1]
    
    for i, weight in enumerate(rw):
        obj.rowconfigure(i, weight=weight)
    for i, weight in enumerate(cw):
        obj.columnconfigure(i, weight=weight)
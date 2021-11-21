# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 14:52:38 2021

@author: Brian
"""

import tkinter as tk

# For scaling everything up/down at once
scale = 4

font = ('Arial', 8*scale)

def default_window(x=1, y=1):
    """Create a Tkinter window. Mostly for testing frames"""
    root = tk.Tk()
    res = [160*scale*x, 144*scale*y] # Original Game Boy Color resolution
    root.geometry(f"{res[0]}x{res[1]}")
    root.title('Pokemon Battle Simulator')
    return root
        
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
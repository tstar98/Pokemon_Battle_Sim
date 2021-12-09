# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:05:28 2021

@author: Brian

A Singleton Subscriber for printing to the console
"""

from Pokemon_Battle_Sim.pubsub import Subscriber, Publisher
from Pokemon_Battle_Sim import use_gui

# Use Python convention to hide constructor
class __ConsolePrinter(Subscriber):
    # Prints any messages to the console
    def update(self, message=''):
        """Prints the given message"""
        print(message)
        
    def flush(self):
        pass # Just needed to match GUIPrinter interface
ConsolePrinter = __ConsolePrinter()

class __GUIPrinter(Subscriber, Publisher):
	# Prints any messages to the appropriate textbox
    # Mostly serves as a pass-through and bundler so that other scripts can 
    # access it as a singleton, then it publishes whatever GUI is open
    def __init__(self):
        self.q = [] # I get tired of remembering how to spell "queue" so it's q
        
        # Initialize the Publisher
        Publisher.__init__(self)
        
        # Initialize the Subscriber
        Subscriber.__init__(self)
        
    def update(self, message=''):
        """Enqueues the message"""
        self.q.append(message)
        
        # Also print to console
        ConsolePrinter.update(message)
        
    def flush(self):
        """Print all the queued messages"""
        self.publish('\n'.join(self.q))
        self.q.clear()
GUIPrinter = __GUIPrinter()

# Choose the appropriate default printer
# Don't hide the base printers, in case something wants to force-print to console
if use_gui:
    Printer = GUIPrinter
else:
    Printer = ConsolePrinter
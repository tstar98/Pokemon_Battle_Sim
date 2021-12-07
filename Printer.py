# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:05:28 2021

@author: Brian

A Singleton Subscriber for printing to the console
"""

from Pokemon_Battle_Sim.pubsub import Subscriber
from Pokemon_Battle_Sim import use_gui

# Use Python convention to hide constructor
class __ConsolePrinter(Subscriber):
    def update(self, message):
        """Prints the given message"""
        print(message)
ConsolePrinter = __ConsolePrinter()

class __GUIPrinter(Subscriber):
    def update(self, message):
        # TODO use text boxes instead
        """Prints the given message"""
        print(message)
GUIPrinter = __GUIPrinter()

# Choose the appropriate default printer
# Don't hide the base printers, in case something wants to force-print to console
if use_gui:
    Printer = GUIPrinter
else:
    Printer = ConsolePrinter
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 15:30:21 2021

@author: Brian
"""

import tkinter as tk

import util
from Pokemon_Battle_Sim.database import database as db
from Pokemon_Battle_Sim.pubsub import Publisher, Subscriber
from Pokemon_Battle_Sim.pokemon import Pokemon
from Pokemon_Battle_Sim.moves.move import Move, move_factory, get_learnset

class team_select(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        util.gridconfigure(self, rw=[1, 10, 10, 5], cw=[1, 1, 1, 1])
        
        # Back button (top left)
        def command():
            try:
                self.master.open_menu("MAIN MENU")
            except AttributeError:
                print("Go back to main menu")
        back = util.Button(self, text="Main Menu", command=command)
        back['font'] = (util.font[0], 10) # Not sure why "font" kwarg doesn't seem to work
        back.grid(row=0, column=0, sticky='NSW')
        
        # Search bar (top right)
        search = tk.Label(self, text="Search (WIP)", font=('Arial', 20))
        search.grid(row=0, column=1, columnspan=3, sticky='NSE')
        
        # Pokemon list (center left)
        plist = self.pokemon_list(self, bg='yellow')
        plist.grid(row=1, rowspan=2, column=0, columnspan=1, sticky='NSEW')
        
        # Pokemon detail (center right upper)
        pdetail = self.pokemon_detail(self, bg='red')
        pdetail.grid(row=1, column=1, columnspan=3, sticky='NSEW')
        
        # Move selection (center right lower)
        mselect = self.move_select(self, bg='blue')
        mselect.grid(row=2, column=1, columnspan=3, sticky='NSEW')
        
        # Add move button
        # Needs to be on the same level as Move Selection and Pokemon Detail for easier passing
        add_move = self.add_move(self)
        add_move.grid(row=2, column=3, sticky='SE')
        
        # Connect Publishers and Subscribers
        plist.add_subscriber(pdetail)
        plist.add_subscriber(mselect)
        add_move.add_subscriber(pdetail)
        mselect.mlist.add_subscriber(add_move)
        
        # Current team (bottom)
        team = tk.Frame(self, bg='cyan')
        team.grid(row=3, column=0, columnspan=4, sticky='NSEW')
        
    class add_move(tk.Button, Publisher, Subscriber):
        def __init__(self, parent, *args, **kwargs):
            # self = util.Button(parent, text='Add Move', command=self.command,
            #                  *args, **kwargs)
            # FIXME why doesn't this work?
            super().__init__(parent, text='Add Move', command=self.command,
                             *args, **kwargs)
            self.move = None
            
            # Initialize Publisher
            Publisher.__init__(self)
            
            # Initialize Subscriber
            Subscriber.__init__(self)
            
        def update(self, message):
            self.move = message
            
        def command(self):
            if self.move is None:
                pass
            else:
                # Send the current move to the Pokemon
                self.publish(self.move)
        
    class pokemon_list(tk.Listbox, Publisher):
        """
        Source: https://www.pythontutorial.net/tkinter/tkinter-listbox/
        """
        def __init__(self, parent, *args, **kwargs):
            # Create the StringVar list that is displayed
            self.full_list = db.select("SELECT id, name FROM pokemon")
            namelist = tk.StringVar(value=[f"{x[0]}.{x[1]}" for x in self.full_list])
            # Create the ListBox
            font = (util.font[0], int(0.5*util.font[1]))
            super().__init__(parent, listvariable=namelist, selectmode=tk.SINGLE,
                             font=font, width=0,
                             *args, **kwargs)
            self.grid(row=0, column=0)
            # Assign behavior when selecting
            self.bind("<<ListboxSelect>>", self.select)
            
            # Initialize Publisher
            Publisher.__init__(self)
            
        def select(self, event):
            selection = self.curselection()
            if len(selection) == 0:
                # Was actually a de-select
                return
            else:
                idx, = selection
                pid = self.full_list[idx][0]
                self.publish(Pokemon(pid))
            
    class pokemon_detail(tk.Frame, Subscriber):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            util.gridconfigure(self, rw=[1, 1], cw=[1,1,1,1])
            self.pokemon = None
            
            # Pokemon info
            self.text = tk.Label(self, text='Select a Pokemon on the left')
            self.text.grid(row=0, column=0, columnspan=4, sticky='NSEW')
            
            # Add Pokemon button
            button = tk.Button(self, text='Add to Team', command=self.add_pokemon)
            button.grid(row=0, column=3, sticky='NE')
            
            # Moves
            self.moves = []
            self.move_buttons = []
            for col in range(4):
                button = util.Button(self)
                button.grid(row=1, column=col, sticky='NSEW')
                self.move_buttons.append(button)
            
            # Initialize Subscriber
            Subscriber.__init__(self)
            
        def add_pokemon(self):
            if self.pokemon is None:
                pass
            else:
                print(f"Adding {self.pokemon.name} to team")
                
                # TODO Clear current pokemon/move selections
            
        def update(self, message):
            if isinstance(message, Pokemon):
                self.pokemon = message
                self.text['text'] = message.name
                self.moves.clear()
                for button in self.move_buttons:
                    button['text'] = ''
            elif isinstance(message, Move):
                if len(self.moves) == 4:
                    raise RuntimeError("Too many moves")
                button = self.move_buttons[len(self.moves)]
                self.moves.append(message)
                button['text'] = message.name
            else:
                raise TypeError()
            
    class move_select(tk.Frame, Subscriber):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            util.gridconfigure(self, cw=[1, 3])
            self.mlist = self.move_list(self)
            self.mlist.grid(row=0, column=0, sticky='NESW')
            self.mdetail = self.move_detail(self)
            self.mdetail.grid(row=0, column=1, sticky='NESW')
        
            # Connect list to detail
            self.mlist.add_subscriber(self.mdetail)
                
            # Initialize Subscriber
            Subscriber.__init__(self)
            
        def update(self, pokemon):
            self.mlist.update(pokemon)
            
        class move_list(tk.Listbox, Publisher, Subscriber):
            """
            Source: https://www.pythontutorial.net/tkinter/tkinter-listbox/
            """
            def __init__(self, parent, *args, **kwargs):
                self.namelist = [] # Makes life easier to store move names
                # Create the StringVar list that is displayed
                self.listvariable = tk.StringVar(value='')
                # Create the ListBox
                font = (util.font[0], int(0.3*util.font[1]))
                super().__init__(parent, listvariable=self.listvariable, selectmode=tk.SINGLE,
                                 font=font, width=0,
                                 *args, **kwargs)
                self.grid(row=0, column=0)
                # Assign behavior when selecting
                self.bind("<<ListboxSelect>>", self.select)
            
                # Initialize Publisher
                Publisher.__init__(self)
                
                # Initialize Subscriber
                Subscriber.__init__(self)
            
            def select(self, event): # Publish
                """Get the current selection and publish it"""
                selection = self.curselection()
                if len(selection) == 0:
                    # Was actually a de-select
                    self.publish(None)
                else:
                    idx, = selection
                    name = self.namelist[idx]
                    self.publish(move_factory(name))
                
            def update(self, pokemon):
                self.namelist = get_learnset(pokemon.pokemon_id)
                self.listvariable.set(self.namelist)
            
        class move_detail(tk.Frame, Subscriber):
            def __init__(self, parent, *args, **kwargs):
                super().__init__(parent, *args, **kwargs)
                self.text = tk.Label(self, text='Select a move on the left')
                self.text.grid(row=0, column=0, sticky='NSEW')
                
                # Initialize Subscriber
                Subscriber.__init__(self)
                
            def update(self, message):
                if message is None:
                    self.text['text'] = 'Select a move on the left'
                else:
                    self.text['text'] = message.name
            
        
if __name__ == "__main__":
    root = util.default_window()
    util.gridconfigure(root)
    menu = team_select(root)
    menu.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()
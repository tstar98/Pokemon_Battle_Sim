# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 15:30:21 2021

@author: Brian
"""

import itertools
import tkinter as tk

from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.database import database as db
from Pokemon_Battle_Sim.pubsub import Subscriber, Observer
from Pokemon_Battle_Sim.pokemon import Pokemon
from Pokemon_Battle_Sim.moves.move import Move, move_factory, get_learnset
from Pokemon_Battle_Sim.Model import Model, channels
from Pokemon_Battle_Sim import MAX_TEAM, MAX_MOVES
from Pokemon_Battle_Sim.Trainer import channels as trainer_channels

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
        
        # Current team (bottom)
        team = self.Current_Team(self, bg='cyan')
        team.grid(row=3, column=0, columnspan=4, sticky='NSEW')
        
    class add_move(tk.Button):
        def __init__(self, parent, *args, **kwargs):
            # self = util.Button(parent, text='Add Move', command=self.command,
            #                  *args, **kwargs)
            # FIXME why doesn't this work?
            super().__init__(parent, text='Add Move', command=self.command,
                             *args, **kwargs)
            
        def command(self):
            if Model.sel_move is None:
                pass
            else:
                # Add the current move to the Pokemon
                Model.add_sel_move()
        
    class pokemon_list(tk.Listbox):
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
            
        def select(self, event):
            selection = self.curselection()
            if len(selection) == 0:
                # Was actually a de-select
                return
            else:
                idx, = selection
                pid = self.full_list[idx][0]
                old_id = Model.sel_pokemon.pokemon_id
                if pid == old_id:
                    # Reselected what was already selected, do nothing
                    pass
                else:
                    # Selection changed
                    Model.set_sel_pokemon(Pokemon(pid))
            
    class pokemon_detail(tk.Frame, Subscriber):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            util.gridconfigure(self, rw=[1, 1], cw=[1,1,1,1])
            
            # Pokemon info
            self.text = tk.Label(self, text='Select a Pokemon on the left')
            self.text.grid(row=0, column=0, columnspan=4, sticky='NSEW')
            
            # Add Pokemon button
            button = tk.Button(self, text='Add to Team', command=self.add_pokemon)
            button.grid(row=0, column=3, sticky='NE')
            
            # Moves
            self.move_buttons = []
            for col in range(MAX_MOVES):
                button = util.Button(self)
                button.grid(row=1, column=col, sticky='NSEW')
                self.move_buttons.append(button)
            
            # Initialize Subscriber
            Subscriber.__init__(self)
            Model.add_subscriber(channels.SELECTED_POKEMON, self)
            
        def add_pokemon(self):
            if Model.sel_pokemon is None:
                pass
            else:
                Model.player.add_to_team(Model.sel_pokemon)
                # TODO Clear current pokemon/move selections
            
        def update(self, pokemon):
            if Pokemon is None:
                self.text['text'] = 'Select a Pokemon on the left'
            else:
                self.text['text'] = pokemon.name
                for move, button in itertools.zip_longest(pokemon.moves, self.move_buttons):
                    if move is None:
                        button['text'] = ''
                    else:
                        button['text'] = move.name
            
    class move_select(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            util.gridconfigure(self, cw=[1, 3])
            self.mlist = self.move_list(self)
            self.mlist.grid(row=0, column=0, sticky='NESW')
            self.mdetail = self.move_detail(self)
            self.mdetail.grid(row=0, column=1, sticky='NESW')
            
        class move_list(tk.Listbox, Subscriber):
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
                
                # Initialize Subscriber
                Subscriber.__init__(self)
                Model.add_subscriber(channels.SELECTED_POKEMON, self)
            
            def select(self, event):
                """Get the current selection and update the Model with it"""
                selection = self.curselection()
                if len(selection) == 0:
                    # Was actually a de-select
                    Model.set_sel_move(None)
                else:
                    idx, = selection
                    name = self.namelist[idx]
                    Model.set_sel_move(move_factory(name))
                
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
                Model.add_subscriber(channels.SELECTED_MOVE, self)
                
            def update(self, message):
                if message is None:
                    self.text['text'] = 'Select a move on the left'
                else:
                    self.text['text'] = message.name
            
    class Current_Team(tk.Frame, Observer):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            util.gridconfigure(self, cw=[1]*MAX_TEAM)
            
            self.details = []
            for i in range(MAX_TEAM):
                frame = util.Frame(self)
                util.grid(frame, column=i)
                self.details.append(frame)
            
            # Initialize the Observer
            Observer.__init__(self, Model.player, trainer_channels.TEAM)
        
        def update(self, message=None):
            if message == "append":
                # Only need to add a new Pokemon
                i = len(Model.player.team()) - 1
                frame = self.details[i]
                pokemon = Model.player.team()[-1]
                
                util.gridconfigure(frame, rw=[2, 1, 1,1,1,1])
                
                # Name
                name = tk.Label(frame, text=pokemon.name)
                util.grid(name, row=0)
                
                # Types
                # TODO
                types = tk.Label(frame, text='TODO: types')
                util.grid(types, row=1)
                
                # Moves
                for i, move in enumerate(pokemon.moves):
                    label = tk.Label(frame, text=move.name)
                    util.grid(label, row=i+2)
                # Fill in unused moves
                for ii in range(i+1, MAX_MOVES):
                    label = tk.Label(frame, text='')
                    util.grid(label, row=ii+2)
                
            else:
                raise NotImplementedError()
    
if __name__ == "__main__":
    root = util.Default_Window()
    util.gridconfigure(root)
    menu = team_select(root)
    menu.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()
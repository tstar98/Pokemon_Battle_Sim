import math
from enum import Enum
import enums
from Pokemon_Battle_Sim.pubsub import ChannelObservable
from Pokemon_Battle_Sim import use_gui, MAX_TEAM
# from Pokemon_Battle_Sim.Model import Model # just-in-time import to avoid circular import
from Pokemon_Battle_Sim.Printer import Printer

class channels(Enum):
    PRINT = "PRINT"
    TEAM = "TEAM"
    
class Trainer(ChannelObservable):
    def __init__(self):
        self._team = []
        self._reflect = 0
        self._light_screen = 0
        self._max_team = MAX_TEAM
        
        super().__init__()
        for channel in channels:
            self.add_channel(channel)
        # Publish PRINT channel to Printer for printing Reflect and Light Screen effects
        self.add_subscriber(channels.PRINT, Printer)

    def add_to_team(self, pokemon):
        if len(self._team) < self._max_team:
            self._team.append(pokemon)
            pokemon.add_subscriber(Printer)
            self.publish(channels.TEAM, "append")
            return True
        else:
            return False

    # abstract function to be implemented in subclass
    def make_selection(self):
        """ trainer makes selection to either fight or switch """
        raise NotImplementedError()

    def random_move(self):
        return self.pokemon_out().get_random_move()

    def next_turn(self):
        """performs functions that occur in between turns"""
        self._light_screen = 0 if self._light_screen <= 0 else self._light_screen - 1
        self._reflect = 0 if self._reflect <= 0 else self._reflect - 1

    def team(self):
        return self._team

    def pokemon_out(self):
        return self._team[0]

    def has_pokemon(self):
        for pokemon in self._team:
            if pokemon.hp > 0:
                return True
        return False

    def switch_pokemon(self, pokemon):
        """Switches pokemon_out with given pokemon"""
        self.publish(f"{self._team[0].name} was removed from battle.")

        i = self._team.index(pokemon)
        self._team[0], self._team[i] = self._team[i], self._team[0]
        
        self.publish(channels.TEAM, "switched")

    @property
    def reflect(self):
        return self._reflect

    @reflect.setter
    def reflect(self, value):
        self._reflect = value

    @property
    def light_screen(self):
        return self._light_screen

    @light_screen.setter
    def light_screen(self, value):
        self._light_screen = value


class Player(Trainer):
    def make_selection(self, opponent):
        if use_gui:
            from Pokemon_Battle_Sim.Model import Model # just-in-time import to avoid circular import
            move_use = Model.sel_move
        else:
            move_use = self.pokemon_out().get_random_move()
        return move_use

    def switch_pokemon(self, pokemon):
        super(Player, self).switch_pokemon(pokemon)
        self.publish(f"You sent out {pokemon.name}.")

    @property
    def reflect(self):
        return self._reflect

    @reflect.setter
    def reflect(self, boolean):
        if boolean:
            self.publish("Reflect raised your team's Defense.")
        self._reflect = boolean

    @property
    def light_screen(self):
        return self._light_screen

    @light_screen.setter
    def light_screen(self, boolean):
        if boolean:
            self.publish("Light Screen raised your team's Special.")
        self._reflect = boolean


class Opponent(Trainer):
    def make_selection(self, target_trainer):
        # pokemon1 = self.pokemon_out()
        # pokemon2 = self.pokemon_out()
        # # best_moves = pokemon1.moves()
        #
        # # prefer lowering target's speed if slower than target
        # if pokemon2.speed > pokemon1().speed:
        #     # try paralyzing first (if pokemon has a paralysis move)
        #
        #     # speed lowering move
        #     pass
        #
        # # next, try giving target pokemon a status condition
        # if pokemon2.status_condition == enums.StatusEffect.NONE.value:
        #     pass
        #
        # # heal if below 1/3 health
        # if pokemon1.hp <= math.floor(pokemon1):
        #     pass
        #
        # # choose best attack
        #
        # # return random move if no move has been returned yet
        return self.random_move()

    def switch_pokemon(self, pokemon):
        super(Opponent, self).switch_pokemon(pokemon)
        self.publish(f"Your opponent sent out {pokemon.name}.")

    @property
    def reflect(self):
        return self._reflect

    @reflect.setter
    def reflect(self, boolean):
        if boolean:
            self.publish("Reflect raised your opponent's Defense.")
        self._reflect = boolean

    @property
    def light_screen(self):
        return self._light_screen

    @light_screen.setter
    def light_screen(self, boolean):
        if boolean:
            self.publish("Light Screen raised your opponent's Special.")
        self._reflect = boolean


if __name__ == "__main__":
    print("You're running Trainer again, dummy")
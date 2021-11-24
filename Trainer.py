from Pokemon_Battle_Sim.pubsub import Publisher
from Pokemon_Battle_Sim.gui import battle as battle_gui

class Trainer(Publisher):
    def __init__(self):
        self._team = []
        self._reflect = 0
        self._light_screen = 0
        self._max_team = 3
        self._sub = None

    def add_to_team(self, pokemon):
        if len(self._team) < self._max_team:
            self._team.append(pokemon)
            return True
        else:
            return False

    # abstract function to be implemented in subclass
    def make_selection(self):
        """ trainer makes selection to either fight or switch """
        raise NotImplementedError()

    def next_turn(self):
        """performs functions that occur in between turns"""
        self._light_screen = 0 if self._light_screen <= 0 else self._light_screen - 1
        self._reflect = 0 if self._reflect <= 0 else self._reflect - 1

    def add_subscriber(self, subscriber):
        self._sub = subscriber
        for pokemon in self._team:
            pokemon.add_subscriber(subscriber)

    def remove_subscriber(self):
        self._sub = None
        for pokemon in self._team:
            pokemon.remove_subscriber()

    def publish(self, message):
        self._sub.update(message)

    def team(self):
        return self._team

    def pokemon_out(self):
        return self._team[0]

    def has_pokemon(self):
        for pokemon in self._team:
            if pokemon.hp > 0:
                return True
        return False

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
        
        '''
        Should open the move_select GUI
        Selecting a move should set move_use
        '''
        move_use = battle_gui.open_gui(self.pokemon_out(), opponent)
        
        if move_use is None:
            raise RuntimeError("No move selected")
        
        return move_use


class Opponent(Trainer):
    def make_selection(self, opponent):
        # TODO: Change. For now, it just selects the first move of the pokemon out
        move_use = self._team[0].get_random_move()
        return move_use

if __name__ == "__main__":
    print("You're running Trainer again, dummy")
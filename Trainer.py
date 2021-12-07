from Pokemon_Battle_Sim.pubsub import Publisher, Observable
from Pokemon_Battle_Sim import use_gui, MAX_TEAM

class Trainer(Publisher):
    def __init__(self):
        self._team = self.__Team()
        self._reflect = 0
        self._light_screen = 0
        self._max_team = MAX_TEAM
        self._sub = None
        
    class __Team(list, Observable):
        """Needed to separate the Trainer publishing text from changes to the
        Observable team (i.e. Pokemon added/dropped, switched, etc.)"""
        def __init__(self):
            super().__init__()
            Observable.__init__(self)
            
        def append(self, object, /):
            super().append(object)
            self.publish("append")

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

    def switch_pokemon(self, pokemon):
        """Switches pokemon_out with given pokemon"""
        self.publish(f"{self._team[0].name} was removed from battle.")

        #TODO: remove
        self._team[0].take_damage(1000)

        i = self._team.index(pokemon)
        self._team[0], self._team[i] = self._team[i], self._team[0]

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
            raise NotImplementedError()
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
    def make_selection(self, opponent):
        # TODO: Change. For now, it just selects the first move of the pokemon out
        move_use = self.pokemon_out().get_random_move()
        return move_use

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
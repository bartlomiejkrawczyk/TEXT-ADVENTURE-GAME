from utils.io import (
    load_location_from_configuration,
    load_configuration_from_json,
    write_save_as_json,
    load_save_from_json
)
from entities.player import Player
from entities.equipment import Key
from location.location import Location
from utils.player_input import (
    choose_item_from_dict,
    choose_string,
    player_input
)
from utils.format import print_formatted_list


from typing import List, Dict
import functools


class Game:
    """
    Game class

    Contains attributes:

    :param game: Name of the chosen game, defaults to 'Dungeons and Dragons'
    :type game: str, optional

    :param player: Holds information about player, defaults to None
    :type player: Player, optional

    :param locations: List of locations discovered by player, defaults to None
    :type locations: List[Location], optional

    :param level: The number of location where the player is now, defaults to 1
    :type level: int, optional
    """

    def __init__(self,
                 game: str = 'Dungeons and Dragons',
                 player: Player = None,
                 locations: List[Location] = None,
                 level: int = 1):
        """
        Initialize Game
        """
        self.set_game(game)
        self.set_player(player)
        self.set_locations(locations)
        self.set_level(level)
        self._exit = False

    def as_dict(self) -> Dict:
        """
        Get Game as a dictionary

        :return: Dictionary with game's data
        :rtype: Dict
        """
        return {
            'game': self._game,
            'player': self._player.as_dict(),
            'locations': [location.as_dict() for location in self._locations],
            'level': self._level
        }

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Game':
        """
        Get new Game instance loaded from dictionary

        :param dictionary: Dictionary with game's data
        :type dictionary: Dict
        :return: Game loaded from dictionary
        :rtype: Game
        """
        return Game(
            dictionary['game'],
            Player.from_dict(dictionary['player']),
            [Location.from_dict(location)
             for location in dictionary['locations']],
            dictionary['level']
        )

    # Getters and setters

    def game(self) -> str:
        """
        Get game

        :return: Name of the chosen game
        :rtype: str
        """
        return self._game

    def set_game(self, game: str):
        """
        Set game

        :param game: Name of the chosen game
        :type game: str
        """
        self._game = game

    def player(self) -> Player:
        """
        Get player

        :return: Information about player
        :rtype: Player
        """
        return self._player

    def set_player(self, player: Player):
        """
        Set player

        :param player: Information about player
        :type player: Player
        """
        if player:
            self._player = player
        else:
            self._player = load_configuration_from_json(
                self._game, 'player', Player)

    def locations(self) -> List[Location]:
        """
        Get locations

        :return: List of locations discovered by player
        :rtype: List[Location]
        """
        return self._locations

    def set_locations(self, locations: List[Location]):
        """
        Set locations

        :param locations: List of locations discovered by player
        :type locations: List[Location]
        """
        if locations:
            self._locations = locations
        else:
            self._locations = []
            self.add_location('lvl1')

    def level(self) -> int:
        """
        Get level

        :return: The number of location where the player is now
        :rtype: int
        """
        return self._level

    def set_level(self, level: int):
        """
        Set level

        :param level: The number of location where the player is now
        :type level: int
        """
        self._level = level

    def end(self) -> bool:
        """
        Indicates whether to end the game or start another round

        :return: Value of the exit propery
        :rtype: bool
        """
        return self._exit

    def exit(self):
        """
        Exit the game - set exit property True
        """
        self._exit = True

    def location(self) -> Location:
        """
        Get location where player currently is

        :return: Current location
        :rtype: Location
        """
        return self._locations[self._level-1]

    def __eq__(self, other) -> bool:
        """
        Check if other is equal to self

        :param other: Might be any object
        :type other: Any
        :return: Whether self is equal to other
        :rtype: bool
        """
        return isinstance(other, Game) and self.as_dict() == other.as_dict()

    def add_location(self, filename: str):
        """
        Load location from configuration directory based on filename

        :param filename: Name of loaded location
        :type filename: str
        """
        location = load_location_from_configuration(
            self._game, filename, len(self._locations) + 1)
        self._locations.append(location)

    def save(self):
        """
        Save game state
        """
        print('Enter Save Name:')
        filename = player_input(choose_string)
        write_save_as_json(self._game, filename, self)

    def round(self):
        """
        Round is a single round of the game

        This method is called over and over again in a loop

        During a round player is given set of functions he can call
        """
        player = self.player()
        location = self.location()
        field = location.current_field()

        player_methods = player.available_methods()
        print('\n')
        print('Player Methods:')
        print_formatted_list(player_methods.keys())
        field_methods = field.available_methods(player, self)
        print('Field Methods:')
        print_formatted_list(field_methods.keys())
        location_methods = location.available_methods()
        location_methods = {
            key: functools.partial(item, self._player)
            for key, item in location_methods.items()}
        print('Location Methods:')
        print_formatted_list(location_methods.keys())
        print('Game Methods:')
        game_methods = self.available_methods()
        print_formatted_list(game_methods.keys())
        game_methods.update(player_methods)
        game_methods.update(field_methods)
        game_methods.update(location_methods)
        result = player_input(functools.partial(
            choose_item_from_dict, game_methods))()
        if isinstance(result, Key):
            field.open_with_key(result, self)

    @staticmethod
    def load(game: str, filename: str) -> 'Game':
        """
        Load Game from saves directory

        :return: Name of the save
        :rtype: Game
        """
        return load_save_from_json(game, filename, Game)

    def available_methods(self) -> Dict:
        """
        Get the methods available now to the user

        :return: Dictionary with save and exit functions
        :rtype: Dict
        """
        return {
            'save': self.save,
            'exit': self.exit
        }

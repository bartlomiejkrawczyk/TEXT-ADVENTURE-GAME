from entities.player import Player
from game import Game

from utils.io import (
    load_configuration_from_json,
    load_configuration_from_string
)
from utils.player_input import (
    choose_num_from_list,
    player_input,
    choose_string
)

from typing import List
import functools
import os

GREETINGS = """\t\tWelcome Gamer!
I see you have stumbled upon my Text Adventure Games ;D
Choose a game from the list below:"""


def get_saves_list(filepath: str) -> List[str]:
    """
    Get list of previous saves

    :param filepath: Path to the directory
    :type filepath: str
    :return: List of file names
    :rtype: List[str]
    """

    names = [".".join(f.split(".")[:-1])
             for f in os.listdir(filepath)]
    for num, name in enumerate(names):
        print(f'{num+1}. {name}')
    return names


def get_games_list() -> List[str]:
    """
    Get list of available games
    (games that are specified in the configuration directory)

    :return: List of available games
    :rtype: List[str]
    """
    games = os.listdir("./configuration")
    for num, game in enumerate(games):
        print(f'{num+1}. {game}')
    return games


def new_game(game_name: str) -> Game:
    """
    Setup new game

    :param game_name: Name of the game
    :type game_name: str
    :return: Game loaded from the configuration directory
    :rtype: Game
    """
    print("First of all, chose a name for your character.")
    name = player_input(choose_string)
    print("Let's begin the story...")
    player = load_configuration_from_json(game_name, 'player', Player)
    player.set_name(name)
    game = Game(game_name, player)
    print(load_configuration_from_string(game_name, 'introduction'))
    return game


def load_game(game_name: str) -> Game:
    """
    Load game from previous save

    :param game_name: Name of the game
    :type game_name: str
    :return: Game loaded from the saves directory
    :rtype: Game
    """
    print("You want to load a previous game.")
    path = f'./saves/{game_name}'
    files = []
    if os.path.exists(path):
        files = get_saves_list(path)
    if len(files) == 0:
        print('Wow! Such Empty!')
        print("Let's start a new game instead!")
        return new_game(game_name)
    print('Which number do you want to choose?')
    filename = player_input(
        functools.partial(
            choose_num_from_list,
            files))
    game = Game.load(game_name, filename)
    return game

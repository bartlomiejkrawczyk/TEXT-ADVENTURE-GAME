from location.field import GameOverError
from utils.format import print_break

from setup import (
    GREETINGS,
    get_games_list,
    new_game,
    load_game,
)
from utils.player_input import (
    choose_num_from_list,
    choose_item_from_dict,
    player_input
)

import functools


def main():
    """
    Main function

    Starts the program

    Then loops through the rounds of the game
    """
    print(GREETINGS)
    games = get_games_list()
    print('Which number do you want to choose?')
    game_name = player_input(functools.partial(choose_num_from_list, games))
    print(f'So, you have chosen {game_name}, fantastic!')
    functions = {
        'new game': new_game,
        'load from save': load_game
    }
    print([key.capitalize() for key in functions.keys()])
    game = functools.partial(player_input(
        functools.partial(choose_item_from_dict, functions)),
        game_name)()
    print('\n')
    print(game.player())
    game.location().description()
    try:
        while not game.end():
            print_break()
            game.round()
    except GameOverError as e:
        print('\n')
        print(e)
        print('\n')
    except Exception as e:
        print("Check your game's configuration !!!")
        print(e)


if __name__ == "__main__":
    main()

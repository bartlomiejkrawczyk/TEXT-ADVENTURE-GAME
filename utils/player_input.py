from typing import List, Dict
from collections.abc import Callable


def choose_num_from_list(my_list: List):
    """
    Ask user which number from the list he would like to choose

    :param my_list: List of items
    :type my_list: List
    :raises ValueError: Indicates that user gave word instead of a number
    :raises ValueError: Indicates that the user gave number from outside
                        the list
    :return: Item player has choosen
    :rtype: Any
    """
    num = input('> ')
    if not num.isdigit():
        raise ValueError('Enter a number!')
    num = int(num)-1
    if num not in range(len(my_list)):
        msg = "Don't overthink it, "
        msg += f"enter the number in range [1, {len(my_list)}]"
        raise ValueError(msg)
    return my_list[num]


def choose_item_from_dict(dictionary: Dict):
    """
    Ask user which item from the dicrionary he would like to choose

    :param dictionary: Dictionary
    :type dictionary: Dict
    :raises KeyError: Indicates user gave invalid key
    :return: Item from the dicrionary with given key
    :rtype: Any
    """
    key = input('> ')
    return dictionary[key.lower()]


def choose_string() -> str:
    """
    Ask user to give a string

    :raises ValueError: Indicates that given string was empty
    :return: Given string
    :rtype: str
    """
    string = input('> ')
    if not string:
        raise ValueError(
            "You can't fool me! You have entered an empty String.")
    return string


def player_input(func: Callable):
    """
    Call the function until the player provides correct data

    :param func: Function that needs player input
    :type func: Callable
    :return: Result of the call
    :rtype: Any
    """
    correct = False
    while not correct:
        try:
            result = func()
            correct = True
        except ValueError as e:
            print(e)
        except Exception:
            print("Don't overthink it, enter the correct value")
    return result

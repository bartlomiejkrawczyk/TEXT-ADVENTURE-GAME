import json
from os import mkdir, path
from typing import List

from location.field import Field
from location.location import Location


def load_configuration_from_json(game: str, filename: str, cls):
    """
    Returns object loaded from the configuration directory
    based on the given game name, json file name and class

    :param game: Name of the game
    :type game: str
    :param filename: Name of the config file
    :type filename: str
    :param cls: Class with from_dict static method
    :type cls: class
    :raises FileNotFoundException: Indicates that given file doesn't exist
    :return: Object of a given class
    """
    return load_from_json(f'configuration/{game}/{filename}.json', cls)


def load_configuration_from_string(game: str, filename: str) -> str:
    """
    Returns the value from txt config file

    :param game: Name of the game
    :type game: str
    :param filename: Name of the config file
    :type filename: str
    :raises FileNotFoundException: Indicates that given file doesn't exist
    :return: Config file contents
    :rtype: str
    """
    with open(f'configuration/{game}/{filename}.txt', 'r') as handle:
        return handle.read()


def load_save_from_json(save: str, filename: str, cls):
    """
    Loads save from saves directory

    :param save: Name of the game
    :type save: str
    :param filename: Name of the save
    :type filename: str
    :param cls: Class with from_dict static method
    :type cls: class
    :raises FileNotFoundException: Indicates that given file doesn't exist
    :return: Object of a given class
    """
    return load_from_json(f'saves/{save}/{filename}.json', cls)


def write_save_as_json(save: str, filename: str, obj):
    """
    Save object as json in the saves directory

    :param save: Name of the game
    :type save: str
    :param filename: Name of the save
    :type filename: str
    :param obj: Object with as dict method
    """
    folder_path = f'saves/{save}'
    if not path.exists(folder_path):
        mkdir(folder_path)
    filepath = folder_path + f'/{filename}.json'
    with open(filepath, 'w') as handle:
        json.dump(obj.as_dict(), handle, indent=4)


def load_from_json(path: str, cls=None):
    """
    Reads json file based on path
    If cls is None returns dict else returns object of a given class

    :param path: Path to json file
    :type path: str
    :param cls: Class with from_dict static method, defaults to None
    :type cls: class, optional
    :raises FileNotFoundException: Indicates that given file doesn't exist
    :return: Object of a given class or dict
    """
    with open(path, 'r') as handle:
        result = json.load(handle)
        if cls:
            return cls.from_dict(result)
        else:
            return result


def load_location_from_configuration(game: str,
                                     filename: str,
                                     level: int) -> Location:
    """
    Loads location from the configuration files

    :param game: Name of the game
    :type game: str
    :param filename: Name of the file
    :type filename: str
    :param level: Level of the new location
    :type level: int
    :raises FileNotFoundException: Indicates that given file doesn't exist
    :raises DeformedLocationError: Indicates that loaded location
                                    is not a rectangle
    :raises EmptyLocationError: Indicates that loaded location is empty
    :raises StartingPointNotFoundException: Indicates that in loaded location
                                            starting point is missing
    :return: Loaded location
    :rtype: Location
    """
    path = f'configuration/{game}/fields.json'
    fields = load_from_json(path)
    numbers = load_location(game, filename)
    my_map = []
    for row in numbers:
        new_row = []
        for num in row:
            new_row.append(Field().from_dict(fields[num]))
        my_map.append(new_row)
    return Location(my_map, level=level)


def load_location(game: str, filename: str) -> List[List[int]]:
    """
    Loads location numbers from config file

    :param game: Name of the game
    :type game: str
    :param filename: Name of the file
    :type filename: str
    :raises FileNotFoundException: Indicates that given file doesn't exist
    :return: Matrix of indexes of fields that should be in this position
    :rtype: List[List[int]]
    """
    path = f'configuration/{game}/{filename}.txt'
    with open(path, 'r') as handle:
        numbers = []
        for row in handle.readlines():
            row = [int(num) for num in row.split('\t')]
            numbers.append(row)
        return numbers
